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
        public Point Offset;
        public PSD()
        {
            mPen = new Pen(Color.FromArgb(20,20,20), 6);
            mListPointWithOffset = new List<Point>();
            Offset = new Point();
            Create();
        }

        private List<Point> GetPositionPointsDark()
        {
            List<Point> mListPointDarkOffset = new List<Point>();
            foreach (Point point in mListPointWithOffset) {
                mListPointDarkOffset.Add(new Point(point.X + Offset.X, point.Y + Offset.Y));
            }
            return mListPointDarkOffset;
        }

        public void Create()
        {
            int min_r = 10;
            int max_r = 20;

            // создание точки начала отрезка в 1 или 4 четвертях
            int lenXPSD = rnd_size.Next(min_r, max_r);
            int lenYPSD = rnd_size.Next(min_r, max_r);
            if  (rnd_size.Next(0,2) == 0)
            {
                lenYPSD *= -1;
            }

            mPoints.Add(new Point(lenXPSD, lenYPSD));

            // вычисление нормали к вектору из (0, 0) до созданой точки
            double eXnormal = 1;
            double eYnormal = -((double)lenXPSD/ (double)lenYPSD);

            double lenNormal = Math.Sqrt(eXnormal * eXnormal + eYnormal * eYnormal);
            eXnormal /= lenNormal;
            eYnormal /= lenNormal;

            // создание точки, для искривление отрезка PSD
            int sizeLenNormal = rnd_size.Next(-10, 10);
            int coordXnormal = (int)Math.Round(eXnormal * sizeLenNormal);
            int coordYnormal = (int)Math.Round(eYnormal * sizeLenNormal);

            mPoints.Add(new Point(coordXnormal, coordYnormal));

            // создание точки конца отрезка, симметрично относительно (0, 0)
            mPoints.Add(new Point(-lenXPSD, -lenYPSD));

            int sizeOffset = -4;                   // смещение дополнительной полосы в выпуклую сторону (+ значение) и в внутренюю сторону (- значение)
            if (sizeLenNormal > 0)
            {
                Offset.X = (int)Math.Round(eXnormal * sizeOffset);
                Offset.Y = (int)Math.Round(eYnormal * sizeOffset);
            }
            else
            {
                Offset.X = -(int)Math.Round(eXnormal * sizeOffset);
                Offset.Y = -(int)Math.Round(eYnormal * sizeOffset);
            }

            ChangePositionPoints();
        }

        public override void Draw(Graphics g)
        {

            Pen mPenDarkZone = new Pen(Color.FromArgb(80, 80, 80), mPen.Width * 3);
            g.DrawCurve(mPenDarkZone, GetPositionPointsDark().ToArray());
            g.DrawCurve(mPen, mListPointWithOffset.ToArray());
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
