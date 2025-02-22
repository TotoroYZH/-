import pandas as pd
from pyecharts.charts import Bar, Line
from pyecharts import options as opts

class PyechartsCashFlowDiagram:
    def __init__(self, rd='data.xlsx', sheet_name='Cash Flow Diagram', title='Cash Flow Diagram', show_figure=False, smooth=True):
        self.colors = ['#5470C6','#EE6666','#FAC858','#91CC75']
        self.df = pd.read_excel(rd, sheet_name=sheet_name)
        self.x_data = list(map(str, self.df[self.df.columns[0]].tolist()))
        self.y_data = [[col, self.df[col].tolist()] for col in self.df.columns[1:]]
        self.title = title
        self.show_figure = show_figure
        self.smooth = smooth
        self.bar = Bar()
        self.line = Line()

    def get_color(self):
        self.colors = self.colors[1:] + self.colors[0:1]
        return self.colors[-1]

    def tag_break(self):
        for i in range(1, len(self.x_data)):
            if self.x_data[i-1] != '...' and int(self.x_data[i]) - int(self.x_data[i-1]) > 1:
                self.x_data.insert(i, '...')
                for col in self.y_data[:-1]:
                    col[1].insert(i, None)
                self.y_data[-1][1].insert(i,(self.y_data[-1][1][i]+self.y_data[-1][1][i-1])/2)

    def set_bar(self):
        # 添加 x 轴和 y 轴数据
        self.bar.add_xaxis(self.x_data)
        for col in self.y_data[:-1]:  # 排除最后一列（折线图数据）
            self.bar.add_yaxis(
                series_name=col[0], 
                y_axis=col[1],  # 直接使用 col[1] 作为 y 轴数据
                stack='stack1',
                itemstyle_opts=opts.ItemStyleOpts(color=self.get_color()),
                z_level=1,
                label_opts=opts.LabelOpts(is_show=self.show_figure)
            )
        
        # 确保右侧 Y 轴存在
        self.bar.extend_axis(
            yaxis=opts.AxisOpts(
                name="Total Profit (Billion RMB)",
                position="right",
                axislabel_opts=opts.LabelOpts(color="#000000"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#000000")
                ),
                splitline_opts=opts.SplitLineOpts(is_show=False)
            )
        )
        
        # 标题位置配置
        self.bar.set_global_opts(
            title_opts=opts.TitleOpts(
                title=self.title,
                pos_left="center",
                pos_top="5%",
                title_textstyle_opts=opts.TextStyleOpts(font_size=18)
            ),
            yaxis_opts=opts.AxisOpts(
                name="Income (Billion RMB)",
                position="left",
                axislabel_opts=opts.LabelOpts(color="#000000"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#000000")
                ),
                splitline_opts=opts.SplitLineOpts(is_show=False)
            ),
            # x 轴断点标记
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(
                    formatter="{value}",  # 直接显示 x 轴标签
                    color='#000000'
                ),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#000000")
                )
            )
        )

    def set_line(self):
        # 添加 x 轴和 y 轴数据
        self.line.add_xaxis(self.x_data)
        self.line.add_yaxis(
            series_name=self.y_data[-1][0],
            y_axis=self.y_data[-1][1],
            yaxis_index=1,
            itemstyle_opts=opts.ItemStyleOpts(color=self.get_color()),
            linestyle_opts=opts.LineStyleOpts(width=3),
            symbol="circle",
            symbol_size=10,
            z_level=2,
            label_opts=opts.LabelOpts(is_show=self.show_figure),
            is_smooth=self.smooth,  # 平滑曲线
            # 添加右侧 Y 轴 y=0 横线，并隐藏两端标记
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(y=0)],  # y=0 横线
                linestyle_opts=opts.LineStyleOpts(
                    color="#000000",  # 横线颜色
                    width=1,         # 横线宽度
                    type_="solid"    # 横线类型
                ),
                symbol=["none", "none"],  # 隐藏两端标记
                label_opts=opts.LabelOpts(is_show=False)  # 隐藏标签
            )
        )

    def generate_diagram(self):
        self.tag_break()
        self.set_bar()
        self.set_line()
        self.bar.overlap(self.line)
        self.bar.render('Cash Flow Diagram.html')

if __name__ == '__main__':
    diagram = PyechartsCashFlowDiagram()
    diagram.generate_diagram()
