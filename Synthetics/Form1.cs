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

            int color = random.Next(182, 200);                           // выбор цвета фона
            backgroundСolor = Color.FromArgb(color, color, color);
            currImageViewType = TypeView.layer;
            currCreateType = TypeOrganelle.axon;
            imageSize = new Size(512, 512);
            currView = new Bitmap(imageSize.Width, imageSize.Height);
        }

        /// <summary>
        /// Preview organelles image
        /// </summary>
        Bitmap imagePrew;

        /// <summary>
        /// Last created object which doesn't added to result image
        /// </summary>                                               
        ICompartment LastRemember;

        /// <summary>
        /// Element list
        /// </summary>                                    
        List<ICompartment> compartments = new List<ICompartment>();  ///  добавить в форму для отображения и изменения параметров 

        enum TypeView
        {
            layer,
            maskAxon,
            maskMitoxondrion,
            maskVesicules,
            maskPSD,
            maskMembranes
        }

        enum TypeOrganelle
        {
            axon,
            mitoxondrion,
            PSD,
            membranes,
            vesicles
        }

        /// <summary>
        /// Current view type (image or masks)
        /// </summary>
        TypeView currImageViewType;

        Bitmap currView;
        Bitmap backgroundImg = null;
        Bitmap outer = null;

        /// <summary>
        /// The current object being created type
        /// </summary>                                            
        TypeOrganelle currCreateType;

        Color backgroundСolor;                                       /// добавить в форму для изменения пользователем
        Size imageSize;                                              /// добавить в форму для изменения пользователем через функцию с изменением image

        Random random = new Random();

        public static bool CompareColorR(Color a, Color b)
        {
            return a.R == b.R;
        }
        private bool CheckOverlapNewElement(Bitmap all_mask, Bitmap check_mask, int width, int height)
        {
            for (int y = 0; y < height; ++y)
            {
                for (int x = 0; x < width; ++x)
                {
                    if (!CompareColorR(all_mask.GetPixel(x, y), Color.Black) && !CompareColorR(check_mask.GetPixel(x, y), Color.Black))
                    {
                        return true;
                    }
                }
            }

            return false;
        }
        private void AddNewElementWithoutOverlap(int width, int height, List<ICompartment> compartmentsList, ICompartment newComponent)            ////// Нужна отдельная функция рисования технических масок для отделимости обьектов подальше друг от друга
        {
            Bitmap checkImage = new Bitmap(width, height);
            Bitmap checkNewImage = new Bitmap(width, height);
            Graphics g = Graphics.FromImage(checkImage);
            g.Clear(Color.Black);
            foreach (ICompartment c in compartmentsList)
            {
                if (c.GetType() == typeof(Vesicules))                                                       /// можно обобщить для всех кроме класса PSD и мембран
                {
                    // для обработки окрестности везикул группировать как неделимый кластер
                    Vesicules ves_c = (Vesicules)c;
                    List<Point> ConvexHuLLVesicules = Membrans.GetConvexHull(ves_c.mListPointWithOffset);           /// выглядит криво

                    g.FillClosedCurve(new SolidBrush(Color.White), ConvexHuLLVesicules.ToArray());
                    g.DrawClosedCurve(new Pen(Color.White, ves_c.mSizeCycleMax + 2), ConvexHuLLVesicules.ToArray());
                }
                else if (c.GetType() == typeof(Acson))                                                         /// Без PSD не получается так как мембрана проходит и через них
                {
                    // для обработки Аксона не давать возможности рисовать внутри его
                    Acson acson_c = (Acson)c;
                    g.FillClosedCurve(new SolidBrush(Color.White), acson_c.mListPointWithOffset.ToArray());
                    g.DrawClosedCurve(new Pen(Color.White, 12), acson_c.mListPointWithOffset.ToArray());
                }
                else if (c.GetType() == typeof(PSD))                                                         /// Без дополнительной технической зоны они генерятся слишком близко PSD
                {
                    PSD psd_c = (PSD)c;
                    int addedSizeZone = 16; // увеличить диаметр зоны PSD на 16

                    double unionDiametr = psd_c.lenPSD + addedSizeZone;                                     /// рисую техническую область PSD окружностью
                    int startX = psd_c.mCenterPoint.X - (int)Math.Round(unionDiametr / 2);
                    int startY = psd_c.mCenterPoint.Y - (int)Math.Round(unionDiametr / 2);
                    g.FillEllipse(new SolidBrush(Color.White), startX, startY, (int)Math.Round(unionDiametr), (int)Math.Round(unionDiametr));
                }
                else
                {
                    c.DrawMask(g);
                }
                
            }

            //pictureGeneralBox.Image = checkImage;
            //pictureGeneralBox.Refresh();
            Graphics g2 = Graphics.FromImage(checkNewImage);

            int counter = 0;
            int max_iter = 50;
            do                                                                                                        /// Для нового элнемента блок кода копируется (перенести это и то что выше в функцию и дёргать её
            {
                g2.Clear(Color.Black);
                newComponent.NewPosition(random.Next(5, width-5), random.Next(5, height - 5));

                if (newComponent.GetType() == typeof(Acson))                                                         /// Без PSD не получается так как мембрана проходит и через них
                {
                    // для обработки Аксона не давать возможности рисовать внутри его
                    Acson acson_c = (Acson)newComponent;
                    g2.FillClosedCurve(new SolidBrush(Color.White), acson_c.mListPointWithOffset.ToArray());
                    g2.DrawClosedCurve(new Pen(Color.White, 32), acson_c.mListPointWithOffset.ToArray());
                }
                else if (newComponent.GetType() == typeof(PSD))                                                         /// Без дополнительной технической зоны они генерятся слишком близко PSD
                {
                    PSD psd_c = (PSD)newComponent;
                    int addedSizeZone = 16; // увеличить диаметр зоны PSD на 16

                    double unionDiametr = psd_c.lenPSD + addedSizeZone;                                                   /// рисую техническую область PSD окружностью
                    int startX = psd_c.mCenterPoint.X - (int)Math.Round(unionDiametr / 2);
                    int startY = psd_c.mCenterPoint.Y - (int)Math.Round(unionDiametr / 2);
                    g2.FillEllipse(new SolidBrush(Color.White), startX, startY, (int)Math.Round(unionDiametr), (int)Math.Round(unionDiametr));
                }
                else
                {
                    newComponent.DrawMask(g2);
                }


                ++counter;
            } while (CheckOverlapNewElement(checkImage, checkNewImage, width, height) && counter < max_iter);

            // Добавлено исключение чтобы элементы не накладывались друг на друга
            if (counter == max_iter)
            {
                throw new Exception("Can't add unique position new element");
            }
        }

        private void addNewElementIntoImage(int width, int height)
        {
            // добавление нового изображения если есть
            if (LastRemember != null)
            {
                try
                {
                    // нет смысла проверять мембраны, так как они касаются PSD и будет перекрытие
                    if (LastRemember.GetType() != typeof(Membrans))
                    {
                        AddNewElementWithoutOverlap(width, height, compartments, LastRemember);
                    }
                    compartments.Add(LastRemember);
                    LastRemember = null;

                    //чистка памяти
                    GC.Collect();
                    GC.WaitForPendingFinalizers();
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.Message);
                }
            }
        }

        private void DrawBackround(Bitmap Img, Color ImgСolor)
        {
            Graphics g = Graphics.FromImage(Img);
            // чистка изображения
            g.Clear(ImgСolor);

            PointsNoise p = new PointsNoise();
            p.Draw(g);
            Img = GaussFilter.Process(Img, 7);
            g = Graphics.FromImage(Img);
        }


        /// <summary>
        /// Main DRAW function
        /// </summary>
        private void Draw()
        {
            try
            {
                Type TypeMask = typeof(ICompartment);

                switch (currImageViewType)
                {
                    case TypeView.layer:
                        break;
                    case TypeView.maskAxon:
                        TypeMask = typeof(Acson);
                        break;
                    case TypeView.maskMitoxondrion:
                        TypeMask = typeof(Mitohondrion);
                        break;
                    case TypeView.maskVesicules:
                        TypeMask = typeof(Vesicules);
                        break;
                    case TypeView.maskPSD:
                        TypeMask = typeof(PSD);
                        break;
                    case TypeView.maskMembranes:
                        TypeMask = typeof(Membrans);
                        break;

                    default:
                        throw new Exception("Неизвестный тип отображения в Draw или ошибка в масках");
                }

                Color background = Color.Black; // выбор цвета фона в зависимости маска или изображение
                if (currImageViewType == TypeView.layer)
                {
                    if (backgroundImg == null)
                    {
                        backgroundImg = new Bitmap(imageSize.Width, imageSize.Height);
                        DrawBackround(backgroundImg, backgroundСolor);
                    }
                    currView = new Bitmap(backgroundImg);
                }

                Graphics g = Graphics.FromImage(currView);
                if (currImageViewType != TypeView.layer)
                {
                    g.Clear(Color.Black);
                }

                // рисование в зависимости от типа (изображение или маска)
                foreach (ICompartment c in compartments)
                {
                    if (currImageViewType == TypeView.layer)
                    {
                        c.Draw(g);
                    }
                    else
                    {
                        if (c.GetType() == TypeMask)
                        {
                            c.DrawMask(g);
                        }
                    }
                }

                if (currImageViewType == TypeView.layer)
                {
                    Noise n = new Noise();
                    currView = n.AddGaussianNoise(currView);
                    currView = GaussFilter.Process(currView, 6);
                    currView = n.AddGaussianNoise(currView);
                }

                pictureGeneralBox.Image = currView;
                pictureGeneralBox.Refresh();

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        private void updateViewComponentList()
        {
            listElements.BeginUpdate();
            listElements.Items.Clear();
            foreach (ICompartment c in compartments)
            {
                listElements.Items.Add(c.GetType().Name.ToString());
            }
            listElements.EndUpdate();
        }

        private void generate_Click(object sender, EventArgs e)                                         /// Возможно будет достаточно сделать только функию добавления и рисовки этого объекта и не вызать перерисовку draw
        {
            // добавление нового изображения если есть
            addNewElementIntoImage(imageSize.Width, imageSize.Height);
            Draw();
            updateViewComponentList();

        }

        private void create_organel_Click(object sender, EventArgs e)                                   // Функция создания объектов по параметрам /// не доделана
        {
            try
            {
                if (imagePrew == null)
                {
                    imagePrew = new Bitmap(256, 256);
                }

                Graphics g = Graphics.FromImage(imagePrew);
                g.Clear(Color.White);

                if (LastRemember != null) // перерисовка, чистка памяти
                {
                    LastRemember = null;
                    GC.Collect();
                    GC.WaitForPendingFinalizers();
                }

                switch (currCreateType) /// не все типы ///////////////////
                {
                    case TypeOrganelle.axon:
                        InitializeBackground();
                        LastRemember = new Acson();
                        break;
                    case TypeOrganelle.mitoxondrion:
                        LastRemember = new Mitohondrion();
                        break;
                    case TypeOrganelle.vesicles:
                        LastRemember = new Vesicules();
                        break;
                    case TypeOrganelle.PSD:
                        LastRemember = new PSD();
                        break;
                    case TypeOrganelle.membranes:                                                         /// Добавить после реализации
                        LastRemember = new Membrans(compartments, imageSize);
                        break;

                    default:
                        throw new Exception("Неизвестный тип выбора органеллы в create_organel_Click");
                }


                //рисование в центре изображения
                LastRemember.NewPosition(Convert.ToInt32(g.VisibleClipBounds.Width) / 2,
                                         Convert.ToInt32(g.VisibleClipBounds.Height) / 2);
                LastRemember.Draw(g);

                pictureOrganelsBox.Image = imagePrew;
                pictureOrganelsBox.Refresh();

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        private void InitializeBackground()
        {
            if (backgroundImg == null)
            {
                backgroundImg = new Bitmap(imageSize.Width, imageSize.Height);
                DrawBackround(backgroundImg, backgroundСolor);

                outer = new Bitmap(backgroundImg.Clone(new Rectangle(0, 0, 64, 64), System.Drawing.Imaging.PixelFormat.Format24bppRgb));
                int t = 50;
                for (int x = 0; x < outer.Width; x++)
                    for (int y = 0; y < outer.Height; y++)
                    {
                        int c = outer.GetPixel(x, y).R;
                        if (c > t)
                        {
                            c = c - t;
                        }

                        outer.SetPixel(x, y, Color.FromArgb(c, c, c));
                    }
                Acson.innerTexture = backgroundImg;
                Acson.bubbleTexture = outer;
            }
        }

        private void comboBoxViewType_SelectedIndexChanged(object sender, EventArgs e)     // Функция смены отображения
        {
            try
            {
                ComboBox comboBox = (ComboBox)sender;

                switch (comboBox.SelectedItem.ToString())
                {
                    case "image":
                        currImageViewType = TypeView.layer;
                        break;
                    case "mask axon":
                        currImageViewType = TypeView.maskAxon;
                        break;
                    case "mask mitoxondrion":
                        currImageViewType = TypeView.maskMitoxondrion;
                        break;
                    case "mask vesicules":
                        currImageViewType = TypeView.maskVesicules;
                        break;
                    case "mask PSD":
                        currImageViewType = TypeView.maskPSD;
                        break;
                    case "mask membranes":
                        currImageViewType = TypeView.maskMembranes;
                        break;
                    default:
                        throw new Exception("Неизвестный тип отображения в comboBoxViewType_SelectedIndexChanged");
                }

                Console.WriteLine(currImageViewType);
                Draw();
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        private void comboBoxOrganelsCreate_SelectedIndexChanged(object sender, EventArgs e)   // Функция смены типа создания объекта
        {
            try
            {
                ComboBox comboBox = (ComboBox)sender;

                switch (comboBox.SelectedItem.ToString())
                {
                    case "axon":
                        currCreateType = TypeOrganelle.axon;
                        break;
                    case "mitoxondrion":
                        currCreateType = TypeOrganelle.mitoxondrion;
                        break;
                    case "PSD":
                        currCreateType = TypeOrganelle.PSD;
                        break;
                    case "membrans":
                        currCreateType = TypeOrganelle.membranes;
                        break;
                    case "vesicules":
                        currCreateType = TypeOrganelle.vesicles;
                        break;
                    default:
                        throw new Exception("Неизвестный тип выбора органеллы для создания в comboBoxOrganelsCreate_SelectedIndexChanged");
                }

                Console.WriteLine(currCreateType);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        private void listElements_SelectedIndexChanged(object sender, EventArgs e)                           /// исправить удаление на 2 клик
        {
            try
            {
                int deleteIndedex = listElements.SelectedIndex;
                if (deleteIndedex >= 0)
                {
                    Console.WriteLine($"delete {listElements.SelectedItem} with index {deleteIndedex}");
                    compartments.RemoveAt(listElements.SelectedIndex);
                    updateViewComponentList();
                    Draw();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            // Цикличная генерация
            int count_img = 100;
            Size sizeImageScript = new Size(256, 256);

            // количество элементов на изображении
            int count_PSD = 5;
            int count_Axon = 5;

            // директория сохранения картинок
            string dir_save = "../../Sintetic generation/";
            InitializeBackground();

            for (int counter = 0; counter < count_img; ++counter)
            {
                Console.WriteLine($"{counter + 1} generation img for {count_img}");

                Random rd = new Random();
                int addAcsonAfterMempbran = rd.Next(0, count_Axon - 1);
                // создаю новый список для каждой генерации и очищаю для защиты от оптимизаций
                List<ICompartment> ListGeneration = new List<ICompartment>();
                //ListGeneration.Clear();

                // генерация Axons
                for (int j = 0; j < count_Axon - addAcsonAfterMempbran; ++j)
                {
                    try
                    {
                        ICompartment newAcson = new Acson();
                        AddNewElementWithoutOverlap(sizeImageScript.Width, sizeImageScript.Height, ListGeneration, newAcson);
                        ListGeneration.Add(newAcson);
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine(ex.Message);
                    }
                }

                // генерация PSDs
                for (int i = 0; i < count_PSD; ++i)
                {
                    try
                    {
                        ICompartment newPSD = new PSD();
                        AddNewElementWithoutOverlap(sizeImageScript.Width, sizeImageScript.Height, ListGeneration, newPSD);
                        ListGeneration.Add(newPSD);
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine(ex.Message);
                    }
                }

                // Добавление мембран
                ListGeneration.Add(new Membrans(ListGeneration, sizeImageScript));

                // генерация Аксонов после мембран
                for (int j = 0; j < addAcsonAfterMempbran; ++j)
                {
                    try
                    {
                        ICompartment newAcson = new Acson();
                        AddNewElementWithoutOverlap(sizeImageScript.Width, sizeImageScript.Height, ListGeneration, newAcson);
                        ListGeneration.Add(newAcson);
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine(ex.Message);
                    }
                }


                // Рисование

                // рисование слоя и масок

                // рисование слоя и фона к нему
                Bitmap Img = new Bitmap(sizeImageScript.Width, sizeImageScript.Height);
                DrawBackround(Img, backgroundСolor);
                Graphics gImg = Graphics.FromImage(Img);

                // рисование маски и заплолнение черным
                Bitmap MackAcson = new Bitmap(sizeImageScript.Width, sizeImageScript.Height);
                Graphics gMackAcson = Graphics.FromImage(MackAcson);
                gMackAcson.Clear(Color.Black);

                // рисование маски и заплолнение черным
                Bitmap MackPSD   = new Bitmap(sizeImageScript.Width, sizeImageScript.Height);
                Graphics gMackPSD = Graphics.FromImage(MackPSD);
                gMackPSD.Clear(Color.Black);

                // рисование маски и заплолнение черным
                Bitmap MackMito  = new Bitmap(sizeImageScript.Width, sizeImageScript.Height);
                Graphics gMackMito = Graphics.FromImage(MackMito);
                gMackMito.Clear(Color.Black);

                // рисование маски и заплолнение черным
                Bitmap MackMitoBoarder = new Bitmap(sizeImageScript.Width, sizeImageScript.Height);
                Graphics gMackMitoBoarder = Graphics.FromImage(MackMitoBoarder);
                gMackMitoBoarder.Clear(Color.Black);

                // рисование маски и заплолнение черным
                Bitmap MackMembrans = new Bitmap(sizeImageScript.Width, sizeImageScript.Height);
                Graphics gMackMembrans = Graphics.FromImage(MackMembrans);
                gMackMembrans.Clear(Color.Black);

                // рисование маски и заплолнение черным
                Bitmap MackVesicules = new Bitmap(sizeImageScript.Width, sizeImageScript.Height);
                Graphics gMackVesicules = Graphics.FromImage(MackVesicules);
                gMackVesicules.Clear(Color.Black);

                // рисовка в соответсвующее изображение
                foreach (ICompartment c in ListGeneration)
                {
                    c.Draw(gImg);

                    if (c.GetType() == typeof(PSD))
                    {
                        c.DrawMask(gMackPSD);
                    } 
                    else if (c.GetType() == typeof(Acson))
                    {
                        c.DrawMask(gMackAcson);
                    }
                    else if (c.GetType() == typeof(Membrans))
                    {
                        c.DrawMask(gMackMembrans);
                    }
                    else if (c.GetType() == typeof(Mitohondrion))
                    {
                        c.DrawMask(gMackMito);
                    }
                    else if (c.GetType() == typeof(Vesicules))
                    {
                        c.DrawMask(gMackVesicules);
                    }
                }

                // добавление шума
                Noise n = new Noise();
                Img = n.AddGaussianNoise(Img);
                Img = GaussFilter.Process(Img, 6);
                Img = n.AddGaussianNoise(Img);

                //Сохранение слоя и масок 

                // coхранение слоя 
                Img.Save(dir_save + "original/" + counter.ToString() + ".png", System.Drawing.Imaging.ImageFormat.Png);
                // coхранение маски
                MackPSD.Save(dir_save + "PSD/" + counter.ToString() + ".png", System.Drawing.Imaging.ImageFormat.Png);
                // coхранение маски
                MackAcson.Save(dir_save + "axon/" + counter.ToString() + ".png", System.Drawing.Imaging.ImageFormat.Png);
                // coхранение маски
                MackMembrans.Save(dir_save + "boundaries/" + counter.ToString() + ".png", System.Drawing.Imaging.ImageFormat.Png);
                // coхранение маски
                MackMito.Save(dir_save + "mitochondria/" + counter.ToString() + ".png", System.Drawing.Imaging.ImageFormat.Png);
                // coхранение маски
                MackVesicules.Save(dir_save + "vesicles/" + counter.ToString() + ".png", System.Drawing.Imaging.ImageFormat.Png);
                // coхранение маски
                MackMitoBoarder.Save(dir_save + "mitochondrial boundaries/" + counter.ToString() + ".png", System.Drawing.Imaging.ImageFormat.Png);
                // coхранение маски

            }
        }
    }
}
