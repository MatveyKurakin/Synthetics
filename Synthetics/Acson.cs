﻿using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Synthetics
{
    class Acson : ICompartment
    {
        public Acson()
        {
            center_point = new Point(0, 0);
            size_point = 0;
            Points = new List<Point>();
            pen = new Pen(Color.Black, 6);

            ListPointWithOffset = new List<Point>();

            Create();
        }
        public Acson(int min_r, int max_r, int size_angle)
        {
            center_point = new Point(0, 0);
            size_point = size_angle;
            Points = new List<Point>();
            pen = new Pen(Color.Black, 6);

            ListPointWithOffset = new List<Point>();

            Create(min_r, max_r);
        }
        public void Create(int min_r = 0, int max_r = 0)
        {
            Points.Clear();
            
            Random rnd_size = new Random();

            if (size_point == 0)
            { 
                size_point = rnd_size.Next(5, 10);
            }

            if (min_r == 0)
            {
                min_r = rnd_size.Next(20, 35);
            }

            if (max_r == 0)
            {
                max_r = rnd_size.Next(35, 65);
            }


            double step_angle = 2.0 * Math.PI / size_point;

            for (int i = 0; i < size_point; ++i)
            {
                double now_angle = step_angle * i;
                int r = rnd_size.Next(min_r, max_r);
                Point now_point = new Point(Convert.ToInt32(Math.Round(r * Math.Sin(now_angle))), Convert.ToInt32(Math.Round(r * Math.Cos(now_angle))));
                Points.Add(now_point);
            }

            ChangePositionPoints();
        }

        public void NewPosition(int x, int y)
        {
            center_point.X = x;
            center_point.Y = y;

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

        private void DrawLine(Graphics g, Pen p)
        {
            for (int i = 1; i < size_point; ++i)
            {
                g.DrawLine(p, ListPointWithOffset[i - 1].X, ListPointWithOffset[i - 1].Y,
                                ListPointWithOffset[i].X, ListPointWithOffset[i].Y);
            }
            g.DrawLine(p, ListPointWithOffset[0].X, ListPointWithOffset[0].Y,
                          ListPointWithOffset[size_point - 1].X, ListPointWithOffset[size_point - 1].Y);
        }
        private void DrawSpline(Graphics g, Pen p)
        {
            g.DrawClosedCurve(p, ListPointWithOffset.ToArray());
        }

        public void Draw(Graphics g) {
            //DrawLine(g, pen);
            DrawSpline(g, pen);
        }
        public void DrawMask(Graphics g)
        {
            Pen mask_pen = (Pen)pen.Clone();
            mask_pen.Color = Color.White;

            DrawLine(g, mask_pen);
        }

        public Pen pen;
        public int size_point;
        public Point center_point;
        public List<Point> Points;
        private List<Point> ListPointWithOffset;
    }
}
