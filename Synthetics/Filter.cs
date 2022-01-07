using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;

namespace Synthetics
{
    class GaussFilter
    {
        private static double[,] kernel;
        private static void generateKernel(int radius)
        {
            kernel = new double[2 * radius + 1, 2 * radius + 1];
            float sigma = (2 * radius + 1) / 3;
            double norm = 0;
            for (int x = -radius; x <= radius; x++)
                for (int y = -radius; y <= radius; y++)
                {
                    kernel[x + radius, y + radius] = Math.Exp(-(x * x + y * y) / (sigma * sigma));
                    norm += kernel[x + radius, y + radius];
                }

            for (int x = 0; x < 2 * radius + 1; x++)
                for (int y = 0; y < 2 * radius + 1; y++)
                {
                    kernel[x, y] /= norm;
                }
        }

        private static int Clamp(int value, int min, int max)
        {
            if (value > max)
                return max;
            else if (value < min)
                return min;
            return value;
        }

        private static double Clamp(double value, double min, double max)
        {
            if (value > max)
                return max;
            else if (value < min)
                return min;
            return value;
        }

        public static Bitmap Process(Bitmap srcImage, int radius)
        {
            generateKernel(radius);
            int width = srcImage.Width;
            int height = srcImage.Height;
            BitmapData srcData = srcImage.LockBits(new Rectangle(0, 0, width, height),
                ImageLockMode.ReadOnly, PixelFormat.Format32bppArgb);
            int bytes = srcData.Stride * srcData.Height;
            byte[] buffer = new byte[bytes];
            byte[] result = new byte[bytes];
            Marshal.Copy(srcData.Scan0, buffer, 0, bytes);
            srcImage.UnlockBits(srcData);
            int colorChannels = 3;
            double[] rgb = new double[colorChannels];

            int kcenter = 0;
            int kpixel = 0;
            for (int y = 0; y < height; y++)
            {
                for (int x = 0; x < width; x++)
                {
                    for (int c = 0; c < colorChannels; c++)
                    {
                        rgb[c] = 0.0;
                    }

                    kcenter = y * srcData.Stride + x * 4;

                    for (int fy = -radius; fy <= radius; fy++)
                        for (int fx = -radius; fx <= radius; fx++)
                        {
                            int idx = Clamp(x + fx, 0, width - 1);
                            int idy = Clamp(y + fy, 0, height - 1);
                            kpixel = idy * srcData.Stride + idx * 4;
                            for (int c = 0; c < colorChannels; c++)
                            {
                                rgb[c] += (double)(buffer[kpixel + c]) * kernel[fy + radius, fx + radius];
                            }
                        }

                    for (int c = 0; c < colorChannels; c++)
                    {
                        rgb[c] = Clamp(rgb[c], 0, 255);
                    }
                    for (int c = 0; c < colorChannels; c++)
                    {
                        result[kcenter + c] = (byte)rgb[c];
                    }
                    result[kcenter + 3] = 255;
                }
            }
            Bitmap resultImage = new Bitmap(width, height);
            BitmapData resultData = resultImage.LockBits(new Rectangle(0, 0, width, height),
                ImageLockMode.WriteOnly, PixelFormat.Format32bppArgb);
            Marshal.Copy(result, 0, resultData.Scan0, bytes);
            resultImage.UnlockBits(resultData);
            return resultImage;
        }
    }
}
