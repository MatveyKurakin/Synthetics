using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Synthetics
{
    class Mitohondrion : Compartment
    {
        public int mSizePoint;
        public Brush brush;

        public Mitohondrion()
        {
            mColor = Color.FromArgb(80, 80, 80);
            mColorCore = Color.Red;
            brush = new SolidBrush(mColorCore);
            mPen = new Pen(mColor, 6);
            mListPointWithOffset = new List<Point>();
            Create();
        }

        public void Create(int min_r = 0, int max_r = 0)
        {
            mSizePoint = 10;
            double step_angle = 2.0 * Math.PI / mSizePoint;

            if (min_r == 0)
            {
                min_r = rnd_size.Next(20, 35);
            }

            if (max_r == 0)
            {
                max_r = rnd_size.Next(35, 65);
            }

            for (int i = 0; i < mSizePoint; ++i)
            {
                double now_angle = step_angle * i;
                int r = rnd_size.Next(min_r, max_r);
                Point now_point = new Point(Convert.ToInt32(Math.Round(r * Math.Sin(now_angle))), Convert.ToInt32(Math.Round(r * Math.Cos(now_angle))));
                mPoints.Add(now_point);
            }

            ChangePositionPoints();
        }

        private void DrawSpline(Graphics g, Pen p, Brush br)
        {
            g.FillClosedCurve(br, mListPointWithOffset.ToArray());
            g.DrawClosedCurve(p, mListPointWithOffset.ToArray());
        }
        public override void Draw(Graphics g)
        {
            DrawSpline(g, mPen, brush);
        }

        protected override void setMaskParam()
        {
            brush = new SolidBrush(Color.White);
            mPen.Color = Color.White;
        }

        protected override void setDrawParam()
        {
            brush = new SolidBrush(mColorCore);
            mPen.Color = mColor;
        }
    }
}
