/*  基于bokeh.js库文件
    使用该文件前请现在html加载相关js文件*/

// 仿真结果数据
var SimResult = {} ;
var Flag_Refresh = {"transient":false,"dc":false,"ac":false} ;

var color_store = ["blue","brown","cyan","green","orange","pink","purple","red","whitesmoke","yellow"];
// create a data source to hold data
// var the_source = new Bokeh.ColumnDataSource({
//     data: { x: [], y: [], color: [] }
// });


function openMode_Bokeh(evt, tabMode) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabMode).style.display = "block";
    evt.currentTarget.className += " active";
};

function plotPoint_tran() {

    if(Flag_Refresh['transient'] == true){
        
        the_source.data.x = [];
        the_source.data.y = [];
        the_source.data.color = [];


        console.log("Flag_Refresh = true !");
        var the_nodes_name = SimResult['transient']["nodes_name"];

        var the_x = SimResult['transient']["time"];
        for(var i=0; i < the_nodes_name.length; i++){
            var the_y = SimResult['transient']["nodes"][the_nodes_name[i]] ;
            the_source.data.x.push(the_x);
            the_source.data.y.push(the_y);
            the_source.data.color.push(color_store[i%color_store.length]);
        }
        the_source.change.emit();
    }
    else{
        alert("The information has not been updated !!!");
    }
};
function plotPoint_dc() {

    if(Flag_Refresh['dc'] == true){
        
        the_source.data.x = [];
        the_source.data.y = [];
        the_source.data.color = [];

        console.log("Flag_Refresh = true !");
        var the_nodes_name = SimResult['dc']["nodes_name"];

        var the_x = SimResult['dc']["sweep"];
        for(var i=0; i < the_nodes_name.length; i++){
            var the_y = SimResult['dc']["nodes"][the_nodes_name[i]] ;
            the_source.data.x.push(the_x);
            the_source.data.y.push(the_y);
            the_source.data.color.push(color_store[i%color_store.length]);
        }
        the_source.change.emit();
    }
    else{
        alert("The information has not been updated !!!");
    }
};
function plotPoint_ac() {

    if(Flag_Refresh['ac'] == true){
        
        the_source.data.x = [];
        the_source.data.y = [];
        the_source.data.color = [];

        console.log("Flag_Refresh = true !");
        var the_nodes_name = SimResult['ac']["nodes_name"];

        var the_x = SimResult['ac']["fre"];
        for(var i=0; i < the_nodes_name.length; i++){
            var the_y = SimResult['ac']["nodes"][the_nodes_name[i]] ;
            the_source.data.x.push(the_x);
            the_source.data.y.push(the_y);
            the_source.data.color.push(color_store[i%color_store.length]);
        }
        the_source.change.emit();
    }
    else{
        alert("The information has not been updated !!!");
    }
};
function PlotSimulationResult(sim_type){
    if(sim_type == "transient"){
        plotPoint_tran();
    }
    else if(sim_type == "dc"){
        plotPoint_dc();
    }
    else if(sim_type == 'ac'){
        plotPoint_ac();
    }
};


function requestSimInfo(sim_type){
    var data = new Object();
    var sim_result ;

    data["sim_type"] = sim_type;
    console.log(sim_type);
    console.log(data);

    $.ajax({
        type: 'POST',
        url: "/getsiminfo",
        data: data,
        async:false,    // 必须关闭异步！！！
        dataType: "json",
        success: function (siminfo) {
            console.log("load sim result successfully !!");
            sim_result = siminfo;
        },
        error: function(){
            alert('ajax post failed !!!');
        }
    });    
    return sim_result ;
};


function Callback_Refresh(sim_type){
    SimResult[sim_type] = requestSimInfo(sim_type);
    Flag_Refresh[sim_type] = true;
};



// bokeh组件相关变量
var bokeh_plot = [] ;
var the_source = {} ;


// 添加 Tab 组件
var sim_mode = ['transient', 'dc', 'ac'];

var div_node = document.createElement('div');
var div_tab = document.createElement('div');
div_tab.setAttribute('class','tab');
div_node.appendChild(div_tab);

var frame = $("#show_result");
frame.append(div_node);


for(var i=0; i<sim_mode.length; i++){
    the_source[sim_mode[i]] = new Bokeh.ColumnDataSource({
        data: { x: [], y: [], color: [] }
    });    
}

// 创建tab
for(var i=0; i<sim_mode.length; i++){
    var div_mode =  document.createElement('button');
    div_mode.setAttribute('class',"tablinks");
    div_mode.setAttribute('onclick',"openMode_Bokeh(event, 'ShowResult"+ sim_mode[i] +"')");

    div_mode.innerHTML = sim_mode[i] ;

    div_tab.appendChild(div_mode);
};

for(var i=0; i<sim_mode.length; i++){
    var div_mode =  document.createElement('div');
    div_mode.setAttribute('class',"tabcontent");
    div_mode.setAttribute('id',"ShowResult"+sim_mode[i]);

    var div_plot = document.createElement('div');
    div_plot.setAttribute('id', 'ResultPlot'+sim_mode[i] );
    div_mode.appendChild(div_plot);


    var div_button = document.createElement('div');
    div_button.setAttribute('id', 'button'+sim_mode[i] );
    div_mode.appendChild(div_button);

    div_node.appendChild(div_mode);

    var RefreshButton = document.createElement("Button");
    RefreshButton.appendChild(document.createTextNode("Refresh"));
    document.currentScript.parentElement.appendChild(RefreshButton);
    // RefreshButton.addEventListener("click", Callback_Refresh);
    RefreshButton.onclick = function(){
        Callback_Refresh(sim_mode[i]);
    };
    div_button.appendChild(RefreshButton);

    var addDataButton = document.createElement("Button");
    addDataButton.appendChild(document.createTextNode("Plot"));
    document.currentScript.parentElement.appendChild(addDataButton);
    // addDataButton.addEventListener("click", plotPoint_tran);
    addDataButton.onclick = function(){
        PlotSimulationResult(sim_mode[i]);
    };
    div_button.appendChild(addDataButton);

    // div_tab.appendChild(div_mode);
};

for(var i=0; i<sim_mode.length; i++){
    bokeh_plot[i] =  Bokeh.Plotting.figure({
        title: sim_mode[i],
        tools: "pan,wheel_zoom,box_zoom,reset,save",
        height: 300,
        width: 400,
        background_fill_color: "#F2F2F7"
    });

    // add a line with data from the source
    bokeh_plot[i].multi_line({field:"x"},{field:"y"},{
        source: the_source[sim_mode[i]],
        color: {field:"color"},
        line_width: 2
    });
    // Bokeh.Plotting.show(bokeh_plot[i],'#ResultPlot'+sim_mode[i]);
};

for(var i=0; i<sim_mode.length; i++){
    Bokeh.Plotting.show(bokeh_plot[i],'#ResultPlot'+sim_mode[i]);
};
