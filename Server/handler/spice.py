from .main import AuthBaseHandler
import tornado.web
from bokeh.embed import server_document
# from jinja2 import Environment, FileSystemLoader

class Spice_1_Handler(AuthBaseHandler):

    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        # env = Environment(loader=FileSystemLoader('template'))
        # template = env.get_template('spice.html')
        # script = server_document('http://localhost:5006/bkapp')
        # self.write(template.render(script=script))

        script = server_document('http://localhost:5006/bkapp')
        self.render('spice/spice1.html',script=script)

class Spice_2_Handler(AuthBaseHandler):
    
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        js_import = """
        <script type="text/javascript" src="https://cdn.bokeh.org/bokeh/release/bokeh-2.2.3.min.js"></script>
        <script type="text/javascript" src="https://cdn.bokeh.org/bokeh/release/bokeh-widgets-2.2.3.min.js"></script>
        <script type="text/javascript" src="https://cdn.bokeh.org/bokeh/release/bokeh-tables-2.2.3.min.js"></script>
        <script type="text/javascript" src="https://cdn.bokeh.org/bokeh/release/bokeh-api-2.2.3.min.js"></script>
        <script type="text/javascript" src="https://cdn.bokeh.org/bokeh/release/bokeh-api-2.2.3.min.js"></script>
        <script type="text/javascript" src="https://cdn.bootcss.com/jquery/3.4.1/jquery.min.js"></script>
        """
        js_code = """
       <script>
        // create a data source to hold data
        var source = new Bokeh.ColumnDataSource({
            data: { x: [], y: [] }
        });

        // make a plot with some tools
        var plot = Bokeh.Plotting.figure({
            title:'Example of Random data',
            tools: "pan,wheel_zoom,box_zoom,reset,save",
            height: 300,
            width: 300
        });

        // add a line with data from the source
        plot.line({ field: "x" }, { field: "y" }, {
            source: source,
            line_width: 2
        });

        // show the plot, appending it to the end of the current section
        Bokeh.Plotting.show(plot);

        function addPoint() {
            // add data --- all fields must be the same length.
            source.data.x.push(Math.random())
            source.data.y.push(Math.random())

            // notify the DataSource of "in-place" changes
            source.change.emit()
        }

        function Callback_Button() {
            addPoint();
                var data = new Object();
                data["name"] = "XerCis";
                data["message"] = "This is the message from ajax(spice2) !";
                $.ajax({
                    type: 'POST',
                    url: "/test",
                    data: data,
                    success: function (response) {
                        alert(response);
                    }
                });

        }
        var addDataButton = document.createElement("Button");
        addDataButton.appendChild(document.createTextNode("Add Some Data!!!"));
        document.currentScript.parentElement.appendChild(addDataButton);
        addDataButton.addEventListener("click", Callback_Button);

        addPoint();
        addPoint();
        </script>
        """
        self.render('spice/spice2.html',js_import=js_import,js_code=js_code)


class Spice_3_Handler(AuthBaseHandler):
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        self.render('spice/spice3.html')


class Spice_4_Handler(AuthBaseHandler):
    @tornado.web.authenticated
    def get(self,*args,**kwargs):
        self.render('spice/spice4.html')