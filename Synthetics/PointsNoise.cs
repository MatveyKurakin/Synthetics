using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Synthetics
{
    class PointsNoise
    {
        protected static Random rnd_size = new Random();
        protected List<Point> mListPointWithOffset = new List<Point>();
        public List<Point> mPoints = new List<Point>();

        public void Create(int min_r = -20, int max_r = 20)
        {
            min_r = rnd_size.Next(min_r, 0);
            max_r = rnd_size.Next(0, max_r);

            for (int i = 0; i < 2; ++i)
            {
                int rx = rnd_size.Next(min_r, max_r);
                int ry = rnd_size.Next(min_r, max_r);
                Point now_point = new Point(rx, ry);
                mPoints.Add(now_point);
            }
        }

        protected void ChangePositionPoints()
        {
            mListPointWithOffset.Clear();
            
            for (int i = 0; i < mPoints.Count; i = i + 2)
            {
                int x = rnd_size.Next(0, 512);
                int y = rnd_size.Next(0, 512);
                mListPointWithOffset.Add(new Point(mPoints[i].X + x, mPoints[i].Y + y));
                mListPointWithOffset.Add(new Point(mPoints[i + 1].X + x, mPoints[i + 1].Y + y));
            }

        }

        public void Draw(Graphics g)
        {
            for(int i = 0; i < 500; i++)
                Create();
            ChangePositionPoints();

            for (int i = 0; i < mListPointWithOffset.Count; i = i + 2)
            {
                int c = rnd_size.Next(100, 159);
                int w = rnd_size.Next(1, 10);
                g.DrawLine(new Pen(Color.FromArgb(c, c, c), w), mListPointWithOffset[i].X, mListPointWithOffset[i].Y,
                                mListPointWithOffset[i + 1].X, mListPointWithOffset[i + 1].Y);
            }
        }
    }
}
