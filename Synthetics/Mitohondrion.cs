using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Synthetics
{
    class Mitohondrion : ICompartment
    { 
        public Mitohondrion()
        {
            center_point = new Point(0, 0);
            Points = new List<Point>();
            pen = new Pen(Color.Black, 6);

            ListPointWithOffset = new List<Point>();
            Create();
        }

        public Mitohondrion(int l)
        {

        }
        public void Create(int min_r = 0, int max_r = 0)
        {

            Random rnd_size = new Random();
            size_point = 10;
            double step_angle = 2.0 * Math.PI / size_point;

            if (min_r == 0)
            {
                min_r = rnd_size.Next(20, 35);
            }

            if (max_r == 0)
            {
                max_r = rnd_size.Next(35, 65);
            }

            for (int i = 0; i < size_point; ++i)
            {
                double now_angle = step_angle * i;
                int r = rnd_size.Next(min_r, max_r);
                Point now_point = new Point(Convert.ToInt32(Math.Round(r * Math.Sin(now_angle))), Convert.ToInt32(Math.Round(r * Math.Cos(now_angle))));
                Points.Add(now_point);
            }

            ChangePositionPoints();
        }

        private void ChangePositionPoints()
        {
            ListPointWithOffset.Clear();
            
            foreach (Point point in Points)
            {
                ListPointWithOffset.Add(new Point(point.X + center_point.X, point.Y + center_point.Y));
            }

        }

        private void DrawSpline(Graphics g, Pen p, Brush br)
        {
            g.FillClosedCurve(br, ListPointWithOffset.ToArray());
            g.DrawClosedCurve(p, ListPointWithOffset.ToArray());
        }
        public void Draw(Graphics g)
        {
            SolidBrush brush = new SolidBrush(Color.Red);
            DrawSpline(g, pen, brush);
        }
        public void NewPosition(int x, int y)
        {
            center_point.X = x;
            center_point.Y = y;

            ChangePositionPoints();
        }
        public void DrawMask(Graphics g)
        {
            SolidBrush brush = new SolidBrush(Color.White);
            Pen mask_pen = (Pen)pen.Clone();
            mask_pen.Color = Color.White;

            DrawSpline(g, mask_pen, brush);

        }

        public Pen pen;
        public int size_point;
        public Point center_point;
        public List<Point> Points;
        private List<Point> ListPointWithOffset;
    }
}
