using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Synthetics
{
    class Vesicules : ICompartment
    { 
        public Vesicules()
        {
            center_point = new Point(0, 0);
            Points = new List<Point>();
            pen = new Pen(Color.Black, 2);
            sizeCycle = new Size(5, 5);
            ListPointWithOffset = new List<Point>();
            Create();
        }

        public Vesicules(int l)
        {

        }
        public void Create(int min_r = 0, int max_r = 0)
        {

            Random rnd_size = new Random();
            size_point = 20;

            if (min_r == 0)
            {
                min_r = rnd_size.Next(-50, 0);
            }

            if (max_r == 0)
            {
                max_r = rnd_size.Next(0, 50);
            }

            for (int i = 0; i < size_point; ++i)
            {
                int rx = rnd_size.Next(min_r, max_r);
                int ry = rnd_size.Next(min_r, max_r);
                Point now_point = new Point(rx, ry);
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

        private void DrawVesicules(Graphics g, Pen p, Brush br)
        {
            foreach (Point point in ListPointWithOffset)
            {
                g.FillEllipse(br, point.X, point.Y, sizeCycle.Width, sizeCycle.Height);
                g.DrawEllipse(p, point.X, point.Y, sizeCycle.Width, sizeCycle.Height);
            }
        }
        public void Draw(Graphics g)
        {
            SolidBrush brush = new SolidBrush(Color.Gray);
            DrawVesicules(g, pen, brush);
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

            DrawVesicules(g, mask_pen, brush);

        }

        public Size sizeCycle;
        public Pen pen;
        public int size_point;
        public Point center_point;
        public List<Point> Points;
        private List<Point> ListPointWithOffset;
    }
}
