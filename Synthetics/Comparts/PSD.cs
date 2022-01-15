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
        public Pen mPenGrayZone;
        public double lenPSD;

        private Color colorGray;
        private SolidBrush mBrushGrayZone;

        public PSD()
        {
            mColor = Color.FromArgb(50, 50, 50);
            colorGray = Color.FromArgb(90, 90, 90);
            mPen = new Pen(mColor, 4);
            mPenGrayZone = new Pen(colorGray, 8);
            mBrushGrayZone = new SolidBrush(colorGray);
            mListPointWithOffset = new List<Point>();
            Create();
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
            float eXnormal = 1;
            float eYnormal = -((float)lenXPSD/ (float)lenYPSD);
            float lenNormal = (float)Math.Sqrt(eXnormal * eXnormal + eYnormal * eYnormal);

            eXnormal /= lenNormal;
            eYnormal /= lenNormal;
            PointF normal = new PointF(eXnormal, eYnormal);


            // создание точки, для искривление отрезка PSD
            int delta = 3;
            int curveVal = rnd_size.Next(-delta, delta);
            Point curvedPoint = new Point((int)Math.Round(normal.X * curveVal), (int)Math.Round(normal.Y * curveVal));
            mPoints.Add(curvedPoint);


            // создание точки конца отрезка, симметрично относительно (0, 0)
            mPoints.Add(new Point(-lenXPSD, -lenYPSD));

            // смещение дополнительной полосы в выпуклую сторону (- значение) и в внутренюю сторону (+ значение)
            int sizeOffset = 3;
            Point Offset = new Point();
            Offset.X = Math.Sign(curveVal) * (int)Math.Round(normal.X * sizeOffset);
            Offset.Y = Math.Sign(curveVal) * (int)Math.Round(normal.Y * sizeOffset);

            Point p1_1 = new Point((int)(mPoints[0].X + Offset.X), (int)(mPoints[0].Y + Offset.Y));
            Point c_1  = new Point((int)(mPoints[1].X + Offset.X), (int)(mPoints[1].Y + Offset.Y));
            Point p2_1 = new Point((int)(mPoints[2].X + Offset.X), (int)(mPoints[2].Y + Offset.Y));

            mPoints.Add(p1_1);
            mPoints.Add(c_1);
            mPoints.Add(p2_1);

            sizeOffset = -12;
            Offset.X = Math.Sign(curveVal) * (int)Math.Round(normal.X * sizeOffset);
            Offset.Y = Math.Sign(curveVal) * (int)Math.Round(normal.Y * sizeOffset);

            mPoints.Add(mPoints[0]);
            Point c_2 = new Point((int)(mPoints[1].X + Offset.X), (int)(mPoints[1].Y + Offset.Y));
            mPoints.Add(c_2);
            mPoints.Add(mPoints[2]);
            mPoints.Add(mPoints[1]);

            lenPSD = Math.Sqrt((4 * lenXPSD * lenXPSD) + (4 * lenYPSD * lenYPSD));
            ChangePositionPoints();
        }

        public override void Draw(Graphics g)
        {
            // затемнение фона позади PSD
            g.DrawCurve(mPenGrayZone, mListPointWithOffset.GetRange(6, 4).ToArray());
            g.FillClosedCurve(mBrushGrayZone, mListPointWithOffset.GetRange(6, 4).ToArray());
            // граница перед PSd
            g.DrawCurve(mPenGrayZone, mListPointWithOffset.GetRange(3, 3).ToArray());
            g.DrawCurve(mPen, mListPointWithOffset.GetRange(0,3).ToArray());

            
            
        }

        protected override void setDrawParam()
        {
            mPen.Color = mColor;
            mPenGrayZone.Color = colorGray;
            mBrushGrayZone = new SolidBrush(colorGray);
        }

        protected override void setMaskParam()
        {
            mPen.Color = Color.White;
            mPenGrayZone.Color = Color.Transparent;
            mBrushGrayZone = new SolidBrush(Color.Black);
        }
    }
}
