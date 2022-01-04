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

        public Membrans()
        {
            mPen = new Pen(Color.FromArgb(80, 80, 80), 6);
            mListPointWithOffset = new List<Point>();
            Create();
        }

        public void Create(int min_r = 0, int max_r = 0)
        {
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
