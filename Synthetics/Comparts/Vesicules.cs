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
        private Color mPenColor = Color.FromArgb(80,80,80);

        public Vesicules()
        {
            mPen = new Pen(mPenColor, 2);
            mSizeCycle = new Size(5, 5);
            mListPointWithOffset = new List<Point>();
            Create();
        }

        public Vesicules(int l)
        {

        }

        private bool CheckOverlap(Point point, double proportion)
        {
            int count = mPoints.Count;
            for (int i = 0; i < count; ++i)
            {
                double x_delt = Math.Abs(mPoints[i].X - point.X);
                double y_delt = Math.Abs(mPoints[i].Y - point.Y);

                if (x_delt / (mSizeCycle.Width + mPen.Width) < proportion ||
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

            if (min_r == 0)
            {
                min_r = rnd_size.Next(-50, 0);
            }

            if (max_r == 0)
            {
                max_r = rnd_size.Next(0, 50);
            }

            int max_iteration = 100000;

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
                    Console.WriteLine("Can't create unique visicul");
                }
                mPoints.Add(now_point);
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
        SolidBrush brush = new SolidBrush(Color.Gray);

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
