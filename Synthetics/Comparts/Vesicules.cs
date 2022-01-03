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

            for (int i = 0; i < mSizePoint; ++i)
            {
                int rx = rnd_size.Next(min_r, max_r);
                int ry = rnd_size.Next(min_r, max_r);
                Point now_point = new Point(rx, ry);
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
