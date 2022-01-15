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
        /// <summary>
        /// Number of circle points
        /// </summary>
        public int mPointNumber;
        public Brush mInnerBrush;
        public Brush mBubbleBrush;
        public int input_radius = 0;

        public Acson()
        {
            mColor = Color.FromArgb(50, 50, 50);
            mColorCore = Color.FromArgb(100, 100, 100);

            int sizePen = rnd_size.Next(12, 14);

            mPen = new Pen(mColor, sizePen);
            mListPointWithOffset = new List<Point>();
            Create();
        }

        public void Create(int min_r = 0, int max_r = 0)
        {
            mPoints.Clear();

            if (mPointNumber == 0)
            { 
                mPointNumber = rnd_size.Next(7, 14);
            }

            if (min_r == 0)
            {
                min_r = rnd_size.Next(60, 70);
            }

            if (max_r == 0)
            {
                max_r = min_r + rnd_size.Next(4, 80);                                  /// лучше поменять параметры
            }

            int max_increase_len = max_r - min_r;

            // 2 типа генерации, если маленький просто оболочка, если большой, то с внутренней частью

            double step_angle = 2.0 * Math.PI / mPointNumber;

            for (int i = 0; i < mPointNumber; ++i)
            {
                double now_angle = step_angle * i;
                int r = min_r + rnd_size.Next(1, max_increase_len);
                Point now_point = new Point(Convert.ToInt32(Math.Round(r * Math.Sin(now_angle))), Convert.ToInt32(Math.Round(r * Math.Cos(now_angle))));
                mPoints.Add(now_point);
            }

            if (min_r > 20)
            {
                input_radius = rnd_size.Next(13, min_r-2);
            }

            ChangePositionPoints();
        }


        public override void Draw(Graphics g)
        {
            g.DrawClosedCurve(mPen, mListPointWithOffset.ToArray());
            Pen pp = (Pen)mPen.Clone();
            pp.Width = rnd_size.Next(15, 20);
            List<Point> sublist = mListPointWithOffset.GetRange(1, 6);
            g.DrawCurve(pp, sublist.ToArray());
            // для 2 типа генерации
            if (input_radius != 0) /// отключено для доработки, так как не работает как должно (поставить != 0)
            {
                //заполнение внутренности
                g.FillClosedCurve(mBubbleBrush, mListPointWithOffset.ToArray());     /// плохо работает и не отрисовывает если после есть обработчик типа рисования окружности.
                
                //очистить центральную внутренность 
                g.FillEllipse(mInnerBrush, mCenterPoint.X - input_radius, mCenterPoint.Y - input_radius, input_radius * 2, input_radius * 2);
                // внутренняя оболочка 
                Pen p = (Pen)mPen.Clone();
                p.Width = 6;
                g.DrawEllipse(p, mCenterPoint.X - input_radius, mCenterPoint.Y - input_radius, input_radius * 2, input_radius * 2);

            }
        }
        protected override void setMaskParam()
        {
            mInnerBrush = new SolidBrush(Color.White);
            mPen.Color = Color.White;
        }

        protected override void setDrawParam()
        {
            mInnerBrush = new SolidBrush(mColorCore);
            mPen.Color = mColor;
        }
    }
}
