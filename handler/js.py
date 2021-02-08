js_import = """
        <script type="text/javascript" src="https://cdn.bokeh.org/bokeh/release/bokeh-2.2.3.min.js"></script>
        <script type="text/javascript" src="https://cdn.bokeh.org/bokeh/release/bokeh-widgets-2.2.3.min.js"></script>
        <script type="text/javascript" src="https://cdn.bokeh.org/bokeh/release/bokeh-tables-2.2.3.min.js"></script>
        <script type="text/javascript" src="https://cdn.bokeh.org/bokeh/release/bokeh-api-2.2.3.min.js"></script>
        <script type="text/javascript" src="https://cdn.bokeh.org/bokeh/release/bokeh-api-2.2.3.min.js"></script>
        <script type="text/javascript" src="https://cdn.bootcss.com/jquery/3.4.1/jquery.min.js"></script>
        """

js_code_1 = """
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