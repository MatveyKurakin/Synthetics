using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Synthetics
{
    abstract class Compartment : ICompartment
    {
        protected Pen mPen;
        protected Pen mMaskPen;
        public Point mCenterPoint;
        protected List<Point> mListPointWithOffset;
        public List<Point> mPoints;

        public abstract void Draw(Graphics g);
        protected abstract void setMaskParam();
        protected abstract void setDrawParam();

        public Compartment()
        {
            mCenterPoint = new Point(0, 0);
            mPoints = new List<Point>();
        }
        
        public void DrawMask(Graphics g)
        {
            setMaskParam();
            Draw(g);
            setDrawParam();
        }

        protected void ChangePositionPoints()
        {
            mListPointWithOffset.Clear();

            foreach (Point point in mPoints)
            {
                mListPointWithOffset.Add(new Point(point.X + mCenterPoint.X, point.Y + mCenterPoint.Y));
            }

        }

        public void NewPosition(int x, int y)
        {
            mCenterPoint.X = x;
            mCenterPoint.Y = y;

            ChangePositionPoints();
        }
    }
}
