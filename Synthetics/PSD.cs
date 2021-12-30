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
        public PSD()
        {
            mPen = new Pen(Color.Black, 8);
        }
        public override void Draw(Graphics g)
        {
            
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
