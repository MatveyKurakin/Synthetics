using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Synthetics
{
    class Acson : ICompartment
    {
        public void Draw(Graphics g)
        {
            g.DrawArc(new Pen(Color.Black, 10), 10, 10, 100, 100, 0, 360);
        }
    }
}
