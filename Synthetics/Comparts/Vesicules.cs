using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Synthetics
{
    class Vesicules : Compartment
    {
        public Size mSizeCycle;
        public int mSizePoint;
        private Color mPenColor = Color.FromArgb(50,50,50);                     /// подобрать цвета

        public Vesicules()
        {
            mPen = new Pen(mPenColor, 3);

            int SizeCycleR = rnd_size.Next(5, 15);                              /// перенести в генерацию
            mSizeCycle = new Size(SizeCycleR, SizeCycleR);
            mListPointWithOffset = new List<Point>();
            Create();
        }

        public Vesicules(int l)                                                 /// заглушка на будущее
        {

        }

        private bool CheckOverlap(Point point, double proportion)
        {
            int count = mPoints.Count;
            foreach (Point mpoint in mPoints)
            {
                double x_delt = (double)Math.Abs(mpoint.X - point.X);
                double y_delt = (double)Math.Abs(mpoint.Y - point.Y);

                if (x_delt / (mSizeCycle.Width + mPen.Width) < proportion &&
                    y_delt / (mSizeCycle.Height + mPen.Width) < proportion)
                {
                    return true;
                }
            }
            return false;
        }
        public void Create(int min_r = 0, int max_r = 0)
        {
            mSizePoint = 20;

            if (min_r == 0)                                                                 /// сделать осмесленную форму генерации
            {
                min_r = rnd_size.Next(-75, 0);
            }

            if (max_r == 0)
            {
                max_r = rnd_size.Next(0, 75);
            }

            int max_iteration = 10000;
            int fail_counter = 0;
            for (int i = 0; i < mSizePoint; ++i)
            {
                int counter = 0;
                Point now_point = new Point();
                do
                {
                    now_point.X = rnd_size.Next(min_r, max_r);
                    now_point.Y = rnd_size.Next(min_r, max_r);
                    ++counter;
                }
                while (CheckOverlap(now_point, 1) && counter < max_iteration);

                if (counter == max_iteration)
                {
                    ++fail_counter;
                }
                mPoints.Add(now_point);
            }

            if (fail_counter != 0)
            {
                Console.WriteLine($"The number of vesicles that could not be generated at a unique position: {fail_counter} out of {mSizePoint}");
            }


            ChangePositionPoints();
        }


        private void DrawVesicules(Graphics g, Pen p, Brush br)
        {
            foreach (Point point in mListPointWithOffset)
            {
                g.FillEllipse(br, point.X, point.Y, mSizeCycle.Width, mSizeCycle.Height);
                g.DrawEllipse(p, point.X, point.Y, mSizeCycle.Width, mSizeCycle.Height);
            }
        }

        Color brushColor = Color.Gray;
        SolidBrush brush = new SolidBrush(Color.FromArgb(192, 192, 192));

        public override void Draw(Graphics g)
        {
            
            DrawVesicules(g, mPen, brush);
        }

        protected override void setMaskParam()
        {
            brushColor = brush.Color;
            brush.Color = Color.White;
            mPen.Color = Color.White;
        }

        protected override void setDrawParam()
        {
            brush.Color = brushColor;
            mPen.Color = mPenColor;
        }


    }
}
