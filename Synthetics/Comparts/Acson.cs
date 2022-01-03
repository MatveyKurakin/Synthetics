using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Synthetics
{
    class Acson : Compartment
    {
        public int mSizePoint;
        

        public Acson()
        {
            mPen = new Pen(Color.Black, 6);
            mListPointWithOffset = new List<Point>();
            Create();
        }

        public Acson(int min_r, int max_r, int size_angle)
        {   
            mSizePoint = size_angle;
            mPen = new Pen(Color.Black, 6);
            mListPointWithOffset = new List<Point>();

            Create(min_r, max_r);
        }

        public void Create(int min_r = 0, int max_r = 0)
        {
            mPoints.Clear();

            if (mSizePoint == 0)
            { 
                mSizePoint = rnd_size.Next(5, 10);
            }

            if (min_r == 0)
            {
                min_r = rnd_size.Next(20, 35);
            }

            if (max_r == 0)
            {
                max_r = rnd_size.Next(35, 65);
            }


            double step_angle = 2.0 * Math.PI / mSizePoint;

            for (int i = 0; i < mSizePoint; ++i)
            {
                double now_angle = step_angle * i;
                int r = rnd_size.Next(min_r, max_r);
                Point now_point = new Point(Convert.ToInt32(Math.Round(r * Math.Sin(now_angle))), Convert.ToInt32(Math.Round(r * Math.Cos(now_angle))));
                mPoints.Add(now_point);
            }

            ChangePositionPoints();
        }

        private void DrawLine(Graphics g, Pen p)
        {
            for (int i = 1; i < mSizePoint; ++i)
            {
                g.DrawLine(p, mListPointWithOffset[i - 1].X, mListPointWithOffset[i - 1].Y,
                                mListPointWithOffset[i].X, mListPointWithOffset[i].Y);
            }
            g.DrawLine(p, mListPointWithOffset[0].X, mListPointWithOffset[0].Y,
                          mListPointWithOffset[mSizePoint - 1].X, mListPointWithOffset[mSizePoint - 1].Y);
        }

        private void DrawSpline(Graphics g, Pen p)
        {
            g.DrawClosedCurve(p, mListPointWithOffset.ToArray());
        }

        public override void Draw(Graphics g) {
            DrawSpline(g, mPen);
        }

        protected override void setMaskParam()
        {
            mPen.Color = Color.White;
        }

        protected override void setDrawParam()
        {
            mPen.Color = Color.Black;
        }
    }
}
