namespace Synthetics
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.Windows.Forms.ListViewItem listViewItem1 = new System.Windows.Forms.ListViewItem("dsad");
            System.Windows.Forms.ListViewItem listViewItem2 = new System.Windows.Forms.ListViewItem("sadsad");
            System.Windows.Forms.ListViewItem listViewItem3 = new System.Windows.Forms.ListViewItem("dsad");
            System.Windows.Forms.ListViewItem listViewItem4 = new System.Windows.Forms.ListViewItem("sadsad");
            this.pictureGeneralBox = new System.Windows.Forms.PictureBox();
            this.generate = new System.Windows.Forms.Button();
            this.ComboBoxOrganelsCreate = new System.Windows.Forms.ComboBox();
            this.pictureOrganelsBox = new System.Windows.Forms.PictureBox();
            this.create = new System.Windows.Forms.Button();
            this.listView1 = new System.Windows.Forms.ListView();
            this.comboBoxViewType = new System.Windows.Forms.ComboBox();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.listView3 = new System.Windows.Forms.ListView();
            this.button2 = new System.Windows.Forms.Button();
            this.listElements = new System.Windows.Forms.ListBox();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.tabControl = new System.Windows.Forms.TabControl();
            this.tabPage1 = new System.Windows.Forms.TabPage();
            this.tabPage2 = new System.Windows.Forms.TabPage();
            ((System.ComponentModel.ISupportInitialize)(this.pictureGeneralBox)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureOrganelsBox)).BeginInit();
            this.groupBox1.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.tabControl.SuspendLayout();
            this.tabPage1.SuspendLayout();
            this.SuspendLayout();
            // 
            // pictureGeneralBox
            // 
            this.pictureGeneralBox.Dock = System.Windows.Forms.DockStyle.Fill;
            this.pictureGeneralBox.Location = new System.Drawing.Point(2, 2);
            this.pictureGeneralBox.Name = "pictureGeneralBox";
            this.pictureGeneralBox.Size = new System.Drawing.Size(630, 496);
            this.pictureGeneralBox.TabIndex = 0;
            this.pictureGeneralBox.TabStop = false;
            // 
            // generate
            // 
            this.generate.Anchor = System.Windows.Forms.AnchorStyles.Bottom;
            this.generate.Location = new System.Drawing.Point(5, 428);
            this.generate.Name = "generate";
            this.generate.Size = new System.Drawing.Size(190, 45);
            this.generate.TabIndex = 1;
            this.generate.Text = "Add";
            this.generate.UseVisualStyleBackColor = true;
            this.generate.Click += new System.EventHandler(this.generate_Click);
            // 
            // ComboBoxOrganelsCreate
            // 
            this.ComboBoxOrganelsCreate.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.ComboBoxOrganelsCreate.FormattingEnabled = true;
            this.ComboBoxOrganelsCreate.Items.AddRange(new object[] {
            "mitoxondrion",
            "axon",
            "PSD",
            "membrans",
            "vesicules"});
            this.ComboBoxOrganelsCreate.Location = new System.Drawing.Point(4, 17);
            this.ComboBoxOrganelsCreate.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.ComboBoxOrganelsCreate.Name = "ComboBoxOrganelsCreate";
            this.ComboBoxOrganelsCreate.Size = new System.Drawing.Size(192, 21);
            this.ComboBoxOrganelsCreate.TabIndex = 3;
            this.ComboBoxOrganelsCreate.Text = "axon";
            this.ComboBoxOrganelsCreate.SelectedIndexChanged += new System.EventHandler(this.comboBoxOrganelsCreate_SelectedIndexChanged);
            // 
            // pictureOrganelsBox
            // 
            this.pictureOrganelsBox.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.pictureOrganelsBox.Location = new System.Drawing.Point(5, 202);
            this.pictureOrganelsBox.Name = "pictureOrganelsBox";
            this.pictureOrganelsBox.Size = new System.Drawing.Size(190, 171);
            this.pictureOrganelsBox.SizeMode = System.Windows.Forms.PictureBoxSizeMode.CenterImage;
            this.pictureOrganelsBox.TabIndex = 4;
            this.pictureOrganelsBox.TabStop = false;
            // 
            // create
            // 
            this.create.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.create.Location = new System.Drawing.Point(4, 379);
            this.create.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.create.Name = "create";
            this.create.Size = new System.Drawing.Size(190, 44);
            this.create.TabIndex = 5;
            this.create.Text = "create organels";
            this.create.UseVisualStyleBackColor = true;
            this.create.Click += new System.EventHandler(this.create_organel_Click);
            // 
            // listView1
            // 
            this.listView1.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.listView1.HideSelection = false;
            listViewItem1.ToolTipText = "wad";
            listViewItem2.ToolTipText = "wdaw";
            this.listView1.Items.AddRange(new System.Windows.Forms.ListViewItem[] {
            listViewItem1,
            listViewItem2});
            this.listView1.Location = new System.Drawing.Point(4, 41);
            this.listView1.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.listView1.Name = "listView1";
            this.listView1.Size = new System.Drawing.Size(192, 156);
            this.listView1.TabIndex = 7;
            this.listView1.UseCompatibleStateImageBehavior = false;
            this.listView1.View = System.Windows.Forms.View.Details;
            // 
            // comboBoxViewType
            // 
            this.comboBoxViewType.FormattingEnabled = true;
            this.comboBoxViewType.Items.AddRange(new object[] {
            "image",
            "mask axon",
            "mask mitoxondrion",
            "mask vesicules",
            "mask PSD"});
            this.comboBoxViewType.Location = new System.Drawing.Point(7, 31);
            this.comboBoxViewType.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.comboBoxViewType.Name = "comboBoxViewType";
            this.comboBoxViewType.Size = new System.Drawing.Size(136, 21);
            this.comboBoxViewType.TabIndex = 8;
            this.comboBoxViewType.Text = "image";
            this.comboBoxViewType.SelectedIndexChanged += new System.EventHandler(this.comboBoxViewType_SelectedIndexChanged);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(4, 13);
            this.label2.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(53, 13);
            this.label2.TabIndex = 9;
            this.label2.Text = "View type";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(4, 53);
            this.label3.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(68, 13);
            this.label3.TabIndex = 10;
            this.label3.Text = "List elements";
            // 
            // listView3
            // 
            this.listView3.HideSelection = false;
            listViewItem3.ToolTipText = "wad";
            listViewItem4.ToolTipText = "wdaw";
            this.listView3.Items.AddRange(new System.Windows.Forms.ListViewItem[] {
            listViewItem3,
            listViewItem4});
            this.listView3.Location = new System.Drawing.Point(8, 207);
            this.listView3.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.listView3.Name = "listView3";
            this.listView3.Size = new System.Drawing.Size(136, 158);
            this.listView3.TabIndex = 12;
            this.listView3.UseCompatibleStateImageBehavior = false;
            this.listView3.View = System.Windows.Forms.View.Details;
            // 
            // button2
            // 
            this.button2.Location = new System.Drawing.Point(8, 375);
            this.button2.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(132, 32);
            this.button2.TabIndex = 13;
            this.button2.Text = "Change param";
            this.button2.UseVisualStyleBackColor = true;
            // 
            // listElements
            // 
            this.listElements.FormattingEnabled = true;
            this.listElements.Location = new System.Drawing.Point(8, 69);
            this.listElements.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.listElements.Name = "listElements";
            this.listElements.Size = new System.Drawing.Size(135, 134);
            this.listElements.TabIndex = 14;
            this.listElements.SelectedIndexChanged += new System.EventHandler(this.listElements_SelectedIndexChanged);
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.ComboBoxOrganelsCreate);
            this.groupBox1.Controls.Add(this.listView1);
            this.groupBox1.Controls.Add(this.pictureOrganelsBox);
            this.groupBox1.Controls.Add(this.create);
            this.groupBox1.Controls.Add(this.generate);
            this.groupBox1.Dock = System.Windows.Forms.DockStyle.Right;
            this.groupBox1.Location = new System.Drawing.Point(792, 0);
            this.groupBox1.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Padding = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.groupBox1.Size = new System.Drawing.Size(200, 526);
            this.groupBox1.TabIndex = 15;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Create compartment";
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.label2);
            this.groupBox2.Controls.Add(this.comboBoxViewType);
            this.groupBox2.Controls.Add(this.button2);
            this.groupBox2.Controls.Add(this.listElements);
            this.groupBox2.Controls.Add(this.listView3);
            this.groupBox2.Controls.Add(this.label3);
            this.groupBox2.Dock = System.Windows.Forms.DockStyle.Left;
            this.groupBox2.Location = new System.Drawing.Point(0, 0);
            this.groupBox2.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Padding = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.groupBox2.Size = new System.Drawing.Size(150, 526);
            this.groupBox2.TabIndex = 16;
            this.groupBox2.TabStop = false;
            // 
            // tabControl
            // 
            this.tabControl.Controls.Add(this.tabPage1);
            this.tabControl.Controls.Add(this.tabPage2);
            this.tabControl.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tabControl.Location = new System.Drawing.Point(150, 0);
            this.tabControl.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.tabControl.Name = "tabControl";
            this.tabControl.SelectedIndex = 0;
            this.tabControl.Size = new System.Drawing.Size(642, 526);
            this.tabControl.TabIndex = 17;
            // 
            // tabPage1
            // 
            this.tabPage1.Controls.Add(this.pictureGeneralBox);
            this.tabPage1.Location = new System.Drawing.Point(4, 22);
            this.tabPage1.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.tabPage1.Name = "tabPage1";
            this.tabPage1.Padding = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.tabPage1.Size = new System.Drawing.Size(634, 500);
            this.tabPage1.TabIndex = 0;
            this.tabPage1.Text = "Layer";
            this.tabPage1.UseVisualStyleBackColor = true;
            // 
            // tabPage2
            // 
            this.tabPage2.Location = new System.Drawing.Point(4, 22);
            this.tabPage2.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.tabPage2.Name = "tabPage2";
            this.tabPage2.Padding = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.tabPage2.Size = new System.Drawing.Size(634, 500);
            this.tabPage2.TabIndex = 1;
            this.tabPage2.Text = "tabPage2";
            this.tabPage2.UseVisualStyleBackColor = true;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(992, 526);
            this.Controls.Add(this.tabControl);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.groupBox1);
            this.Name = "Form1";
            this.Text = "Synthetic";
            ((System.ComponentModel.ISupportInitialize)(this.pictureGeneralBox)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureOrganelsBox)).EndInit();
            this.groupBox1.ResumeLayout(false);
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.tabControl.ResumeLayout(false);
            this.tabPage1.ResumeLayout(false);
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.PictureBox pictureGeneralBox;
        private System.Windows.Forms.Button generate;
        private System.Windows.Forms.ComboBox ComboBoxOrganelsCreate;
        private System.Windows.Forms.PictureBox pictureOrganelsBox;
        private System.Windows.Forms.Button create;
        private System.Windows.Forms.ListView listView1;
        private System.Windows.Forms.ComboBox comboBoxViewType;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.ListView listView3;
        private System.Windows.Forms.Button button2;
        private System.Windows.Forms.ListBox listElements;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.TabControl tabControl;
        private System.Windows.Forms.TabPage tabPage1;
        private System.Windows.Forms.TabPage tabPage2;
    }
}

