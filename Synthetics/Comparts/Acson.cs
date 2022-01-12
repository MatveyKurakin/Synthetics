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
        public Brush brush;
        public int input_radius = 0;

        public Acson()
        {
            mColor = Color.FromArgb(70, 70, 70);
            mColorCore = Color.FromArgb(100, 100, 100);
            mPen = new Pen(mColor, 10);
            mListPointWithOffset = new List<Point>();
            Create();
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
                min_r = rnd_size.Next(10, 30);
            }

            if (max_r == 0)
            {
                max_r = min_r + rnd_size.Next(4, 30);                                  /// лучше поменять параметры
            }

            int max_increase_len = max_r - min_r;

            // 2 типа генерации, если маленький просто оболочка, если большой, то с внутренней частью

            double step_angle = 2.0 * Math.PI / mSizePoint;

            for (int i = 0; i < mSizePoint; ++i)
            {
                double now_angle = step_angle * i;
                int r = min_r + rnd_size.Next(1, max_increase_len);
                Point now_point = new Point(Convert.ToInt32(Math.Round(r * Math.Sin(now_angle))), Convert.ToInt32(Math.Round(r * Math.Cos(now_angle))));
                mPoints.Add(now_point);
            }

            if (min_r > 20)
            {
                input_radius = rnd_size.Next(10, min_r-4);
            }

            ChangePositionPoints();
        }

        private void DrawSpline(Graphics g, Pen p)
        {
            g.DrawClosedCurve(p, mListPointWithOffset.ToArray());
        }

        public override void Draw(Graphics g) {
            DrawSpline(g, mPen);

            // для 2 типа генерации
            if (input_radius == -1) /// отключено для доработки, так как не работает как должно (поставить != 0)
            {
                //заполнение внутренности
                g.FillClosedCurve(brush, mListPointWithOffset.ToArray());     /// плохо работает и не отрисовывает если после есть обработчик типа рисования окружности.
                
                //очистить центральную внутренность 
                g.FillEllipse(new SolidBrush(Color.Transparent), mCenterPoint.X - input_radius, mCenterPoint.Y - input_radius, input_radius * 2, input_radius * 2);
                // внутренняя оболочка 
                g.DrawEllipse(mPen, mCenterPoint.X - input_radius, mCenterPoint.Y - input_radius, input_radius * 2, input_radius * 2);

            }
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
