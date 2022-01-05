using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Synthetics
{
    class Membrans : Compartment
    {
        public int mSizePoint;

        public Membrans(List<ICompartment> compartments, Size sizeImg)
        {
            mPen = new Pen(Color.FromArgb(0, 128, 0), 1);
            mListPointWithOffset = new List<Point>();
            Create(compartments, sizeImg);
        }

        private void RenameRegion(int[,] labels, int ChangeLabel, int NewLabel)
        {
            for (int y = 0; y < labels.GetLength(1); ++y)
            {
                for (int x = 0; x < labels.GetLength(0); ++x)
                {
                    if (labels[y,x] == ChangeLabel)
                    {
                        labels[y,x] = NewLabel;
                    }
                }
            }
        }
        private bool FindName(int[,] labels, int findLabel)
        {
            for (int y = 0; y < labels.GetLength(1); ++y)
            {
                for (int x = 0; x < labels.GetLength(0); ++x)
                {
                    if (labels[y, x] == findLabel)
                    {
                        return true;
                    }
                }
            }
            return false;
        }

        private void RegionCounter(Bitmap img, int[,] labels)
        {
            int label = 0;
            // Цикл по пикселям изображения
            for (int y = 0; y < img.Height; ++y)
            {
                for (int x = 0; x < img.Width; ++x)
                {
                    int kx = x - 1;
                    int B = 0;
                    if (kx <= 0)
                    {
                        kx = 0;
                    }
                    else
                    {
                        B = labels[y,kx];
                    }

                    int ky = y - 1;
                    int C = 0;
                    if (ky <= 0)
                    {
                        ky = 1;
                    }
                    else
                    {
                        C = labels[ky,x];
                    }

                    int A = img.GetPixel(x, y).R;
                    if (A == 0)
                    {
                    }
                    else if (B == 0 & C == 0)
                    {
                        label = label + 1;
                        labels[y,x] = label;
                    }
                    else if (B != 0 & C == 0) {
                        labels[y,x] = B;
                    }
                    else if (B == 0 & C != 0) {
                        labels[y,x] = C;
                    }
                    else if (B != 0 & C != 0) {
                        if (B == C)
                        {
                            labels[y,x] = B;
                        }
                        else
                        {
                            labels[y,x] = B;
                            RenameRegion(labels, C, B);
                        }
                    }
                }
            }
        }


        void ChangeNameRegion(int[,] labels)
        {
            int label = 1;

            while (label != 256)
            {
                if (FindName(labels, label))
                {
                    ++label;
                }
                else
                {
                    int minLabel = -1;
                    for (int y = 0; y < labels.GetLength(1); y++)
                    {
                        if (minLabel != -1)
                        {
                            break;
                        }
                        for (int x = 0; x < labels.GetLength(0); x++)
                            if (labels[y, x] > label)
                            {
                                minLabel = labels[y, x];
                                break;
                            }
                    }
                    if (minLabel != -1)
                    {
                        RenameRegion(labels, minLabel, label);
                        ++label;
                    }
                    else
                    {
                        break;
                    }
                }
            }
            Console.WriteLine($"Max Label {label - 1}");
        }

        Bitmap CreateBitmap(int[,] source)
        {
            ChangeNameRegion(source);
            var bitmap = new Bitmap(source.GetLength(0), source.GetLength(1));
            for (var i = 0; i < bitmap.Height; i++)
                for (var j = 0; j < bitmap.Width; j++)
                    bitmap.SetPixel(i, j, Color.FromArgb(source[i, j], 0, 0)); // вместо Color.FromArgb можете использовать любой другой способ преобразования элемента массива в цвет

            return bitmap;
        }
        public void Create(List<ICompartment> compartments, Size sizeImg)
        {
            Bitmap checkImage = new Bitmap(sizeImg.Width, sizeImg.Height);
            Graphics g = Graphics.FromImage(checkImage);
            g.Clear(Color.Black);
            foreach (ICompartment c in compartments)
            {
                c.DrawMask(g);
            }

            //checkImage.Save("fileMask.png", System.Drawing.Imaging.ImageFormat.Png);

            int[,] labelImage = new int[sizeImg.Height, sizeImg.Width];

            for (int y = 0; y < sizeImg.Height; ++y)
            {
                for (int x = 0; x < sizeImg.Width; ++x)
                {
                    labelImage[y,x] = 0;
                }
            }

            RegionCounter(checkImage, labelImage);
            CreateBitmap(labelImage).Save("file.png", System.Drawing.Imaging.ImageFormat.Png);

            bool repit = true;

            while (repit)
            {
                int[,] LastLabel = (int[,])labelImage.Clone();
                repit = false;
                for (int y = 0; y < sizeImg.Height; ++y)
                {
                    for (int x = 0; x < sizeImg.Width; ++x)
                    {
                        if (LastLabel[y, x] != 0)
                        {
                            int label = LastLabel[y, x];
                            //labelImage[y, x] = label;
                            if (x > 0)
                            {
                                int value = labelImage[y, x - 1];
                                if (value == 0)
                                {
                                    labelImage[y, x - 1] = label;
                                    repit = true;
                                }
                                else if (value != label)
                                {
                                    mPoints.Add(new Point(x, y));
                                }
                            }

                            if (x < sizeImg.Width - 1)
                            {
                                int value = labelImage[y, x + 1];
                                if (value == 0)
                                {
                                    labelImage[y, x + 1] = label;
                                    repit = true;
                                }
                                else if (value != label)
                                {
                                    mPoints.Add(new Point(x, y));
                                }
                            }
                            if (y > 0)
                            {
                                int value = labelImage[y - 1, x];
                                if (value == 0)
                                {
                                    labelImage[y - 1, x] = label;
                                    repit = true;
                                }
                                else if (value != label)
                                {
                                    mPoints.Add(new Point(x, y));
                                }
                            }
                            if (y < sizeImg.Height - 1)
                            {
                                int value = labelImage[y + 1, x];
                                if (value == 0)
                                {
                                    labelImage[y + 1, x] = label;
                                    repit = true;
                                }
                                else if (value != label)
                                {
                                    mPoints.Add(new Point(x, y));
                                }
                            }
                        }
                    }
                }
            }
            Console.WriteLine($"count point = {mPoints.Count}");
        }

        public override void Draw(Graphics g)
        {
            foreach (Point point in mPoints)
            {
                g.DrawLine(mPen, point.X, point.Y, point.X + 1 , point.Y + 1);
            }
        }

        SolidBrush brush = new SolidBrush(Color.Red);
        private Color mPenColor = Color.Red;
        protected override void setMaskParam()
        {
            mPenColor = mPen.Color;
            brush = new SolidBrush(Color.White);
            mPen.Color = Color.White;
        }

        protected override void setDrawParam()
        {
            brush = new SolidBrush(Color.Red);
            mPen.Color = mPenColor;
        }

    }
}
