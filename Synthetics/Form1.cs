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

            Random rd = new Random();
            int color = rd.Next(182, 200);                           // выбор цвета фона
            backgroundСolor = Color.FromArgb(color, color, color);
            nowViewType = TypeView.image;
            nowCreateType = TypeCreate.axon;

            image_size = new Size(512, 512);
        }

        Bitmap imagePrew;                                            // изображения для предпросмотра объекта создания
        ICompartment LastRemember;                                   // Последний созданный объект, который не был добавлен в форму 
        List<ICompartment> compartments = new List<ICompartment>();  // список элементов ///  добавить в форму для отображения и изменения параметров 

        enum TypeView                                                /// сделаны не все типы
        {
            image,
            maskAxon,
            maskMitoxondrion,
            maskVesicules
        }
        enum TypeCreate                                              /// проверить имена типов
        {
            axon,
            mitoxondrion,
            PSD,
            membrans,
            vesicules
        }

        TypeView nowViewType;                                        // Вид отображения {изображения, [маски]} 
        TypeCreate nowCreateType;                                    // Тип создаваемого объекта
        Color backgroundСolor;                                       // Цвет фона /// добавить в форму для изменения пользователем


        Size image_size;                                             /// добавить в форму для изменения пользователем через функцию с изменением image

        Bitmap image;                                                // Хранение основного изображение
        Bitmap maskAxon;                                             // Хранение маски Аксонов
        Bitmap maskMitoxondrion;                                     // Хранение маски Митохондоий
        Bitmap maskVesicules;                                        // Хранение маски Везикул


        private void addNewElementIntoImage(Graphics g)                        /// нормальное добавление а не по случайныи координатам
        {
            // добавление нового изображения если есть
            if (LastRemember != null)
            {
                Random rnd_coord = new Random();
                LastRemember.NewPosition(rnd_coord.Next(0, Convert.ToInt32(g.VisibleClipBounds.Width)),
                                         rnd_coord.Next(0, Convert.ToInt32(g.VisibleClipBounds.Height)));
                compartments.Add(LastRemember);
                LastRemember = null;
            }
        }



        private void Draw()                                          // Основная функция для отрисовки основного поля
        {
            try
            {

                Bitmap now_view; // выбор маски или изображения для рисования в зависимости от ситуации
                Type TypeMask = typeof(ICompartment);

                switch (nowViewType)
                {
                    case TypeView.image:
                        now_view = image;
                        break;

                    case TypeView.maskAxon:
                        now_view = maskAxon;
                        TypeMask = typeof(Acson);
                        break;
                    case TypeView.maskMitoxondrion:
                        now_view = maskMitoxondrion;
                        TypeMask = typeof(Mitohondrion);
                        break;
                    case TypeView.maskVesicules:
                        now_view = maskVesicules;
                        TypeMask = typeof(Vesicules);
                        break;

                    default:
                        throw new Exception("Неизвестный тип отображения в Draw или ошибка в масках");
                }

                if (now_view == null) // создать поле если не создано
                {
                    now_view = new Bitmap(image_size.Width, image_size.Height);
                }

                Color colorPhone; // выбор цвета фона в зависимости маска или изображение
                if (nowViewType != TypeView.image)
                {
                    colorPhone = Color.Black;
                }
                else
                {
                    colorPhone = backgroundСolor;
                }


                // чистка изображения
                for (int x = 0; x < now_view.Width; x++)
                    for (int y = 0; y < now_view.Height; y++)
                    {
                        now_view.SetPixel(x, y, colorPhone);
                    }
                Graphics g = Graphics.FromImage(now_view);

                // добавление нового изображения если есть
                addNewElementIntoImage(g);

                // рисование в зависимости от типа (изображение или маска)
                foreach (ICompartment c in compartments)
                {
                    if (nowViewType == TypeView.image)
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

                // save result                                                                              /// не забыть поправить и тут
                switch (nowViewType)
                {
                    case TypeView.image:
                        image = now_view;
                        break;

                    case TypeView.maskAxon:
                        maskAxon = now_view;
                        break;

                    case TypeView.maskMitoxondrion:
                        maskMitoxondrion = now_view;
                        break;

                    case TypeView.maskVesicules:
                        maskVesicules = now_view;
                        break;

                    default:
                        throw new Exception("Неизвестный тип отображения в Draw. result no save");
                }


                pictureGeneralBox.Image = now_view;
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

                switch (nowCreateType) /// не все типы ///////////////////
                {
                    case TypeCreate.axon:
                        LastRemember = new Acson();
                        break;
                    case TypeCreate.mitoxondrion:
                        LastRemember = new Mitohondrion();
                        break;
                    case TypeCreate.vesicules:
                        LastRemember = new Vesicules();
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

        private void comboBoxViewType_SelectedIndexChanged(object sender, EventArgs e)     // Функция смены отображения /// не доделана
        {
            try
            {
                ComboBox comboBox = (ComboBox)sender;

                switch (comboBox.SelectedItem.ToString())
                {
                    case "image":
                        nowViewType = TypeView.image;
                        break;
                    case "mask axon":
                        nowViewType = TypeView.maskAxon;
                        break;
                    case "mask mitoxondrion":
                        nowViewType = TypeView.maskMitoxondrion;
                        break;
                    case "mask vesicules":
                        nowViewType = TypeView.maskVesicules;
                        break;
                    default:
                        throw new Exception("Неизвестный тип отображения в comboBoxViewType_SelectedIndexChanged");
                }

                Console.WriteLine(nowViewType);
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
                        nowCreateType = TypeCreate.axon;
                        break;
                    case "mitoxondrion":
                        nowCreateType = TypeCreate.mitoxondrion;
                        break;
                    case "PSD":
                        nowCreateType = TypeCreate.PSD;
                        break;
                    case "membrans":
                        nowCreateType = TypeCreate.membrans;
                        break;
                    case "vesicules":
                        nowCreateType = TypeCreate.vesicules;
                        break;
                    default:
                        throw new Exception("Неизвестный тип выбора органеллы для создания в comboBoxOrganelsCreate_SelectedIndexChanged");
                }

                Console.WriteLine(nowCreateType);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
           
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
    }
}
