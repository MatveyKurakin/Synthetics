using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Synthetics
{
    class PSD : Compartment
    {
        public PSD()
        {
            mPen = new Pen(Color.Black, 8);
            mListPointWithOffset = new List<Point>();
            Create();
        }

        public void Create(int min_r = 0, int max_r = 0)
        {   
            if (min_r == 0)
            {
                min_r = rnd_size.Next(-50, 0);
            }

            if (max_r == 0)
            {
                max_r = rnd_size.Next(0, 50);
            }

            for (int i = 0; i < 2; ++i)
            {
                int rx = rnd_size.Next(min_r, max_r);
                int ry = rnd_size.Next(min_r, max_r);
                Point now_point = new Point(rx, ry);
                mPoints.Add(now_point);
            }

            ChangePositionPoints();
        }

        public override void Draw(Graphics g)
        {
            for (int i = 0; i < mListPointWithOffset.Count; i = i + 2)
            { 
                g.DrawLine(mPen, mListPointWithOffset[i].X, mListPointWithOffset[i].Y,
                                mListPointWithOffset[i + 1].X, mListPointWithOffset[i + 1].Y);
            }
        }

        protected override void setDrawParam()
        {
            mPen.Color = Color.Black;
        }

        protected override void setMaskParam()
        {
            mPen.Color = Color.White;
        }
    }
}
