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
        public int mSizeCycleMin;
        public int mSizeCycleMax;
        public int mSizePoint;
        private Color mPenColor = Color.FromArgb(50,50,50);                     /// подобрать цвета
        private List<int> mSizeCycle;

        public Vesicules()
        {
            mPen = new Pen(mPenColor, 3);

            mSizeCycleMin = 5;
            mSizeCycleMax = 12;

            mSizeCycle = new List<int>();
            mListPointWithOffset = new List<Point>();
            Create();
        }

        public Vesicules(int l)                                                 /// заглушка на будущее
        {

        }

        private bool CheckOverlap(Point point, int sizeCycle, double proportion)
        {
            int count = mPoints.Count;

            for (int i = 0; i < count; ++i)
            {
                double x_delt = (double)Math.Abs(mPoints[i].X - point.X);
                double y_delt = (double)Math.Abs(mPoints[i].Y - point.Y);

                if (x_delt / ((mSizeCycle[i] + sizeCycle)/2 + mPen.Width * 2) < proportion &&
                    y_delt / ((mSizeCycle[i] + sizeCycle)/2 + mPen.Width * 2) < proportion)
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
                int nowSizeCycle;
                do
                {
                    nowSizeCycle = rnd_size.Next(mSizeCycleMin, mSizeCycleMax);
                    now_point.X = rnd_size.Next(min_r, max_r);
                    now_point.Y = rnd_size.Next(min_r, max_r);

                    ++counter;
                }
                while (CheckOverlap(now_point, nowSizeCycle, 1) && counter < max_iteration);

                if (counter == max_iteration)
                {
                    ++fail_counter;
                }
                mSizeCycle.Add(nowSizeCycle);
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
            for (int i = 0; i < mListPointWithOffset.Count; ++i)
            {
                g.FillEllipse(br, mListPointWithOffset[i].X, mListPointWithOffset[i].Y, mSizeCycle[i], mSizeCycle[i]);
                g.DrawEllipse(p, mListPointWithOffset[i].X, mListPointWithOffset[i].Y, mSizeCycle[i], mSizeCycle[i]);
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
