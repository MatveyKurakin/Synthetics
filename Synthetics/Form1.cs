using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Synthetics
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            compartments.Add(new Acson());
        }

        Bitmap image;
        List<ICompartment> compartments = new List<ICompartment>(); 

        private void generate_Click(object sender, EventArgs e)
        {
            image = new Bitmap(800, 600);
            for(int x = 0; x < image.Width; x++)
                for(int y =  0; y < image.Height; y++)
                {
                    image.SetPixel(x, y, Color.LightGray);
                }
            Graphics g = Graphics.FromImage(image);
            foreach(ICompartment c in compartments)
            {
                c.Draw(g);
            }
            pictureBox.Image = image;
            pictureBox.Refresh();
        }
    }
}
