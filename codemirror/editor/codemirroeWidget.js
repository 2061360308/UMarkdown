window.onresize = resize;

function resize() {
    let widgetWidth = document.documentElement.clientWidth;
    editorElm.setAttribute("style", "width:" + widgetWidth.toString() + "px;")
}

function webSort() {
    let userAgent = navigator.userAgent; //取得浏览器的userAgent字符串
    let isOpera = userAgent.indexOf("Opera") > -1;
    if (isOpera) {
        return "Opera";
    } //判断是否Opera浏览器
    if (userAgent.indexOf("Firefox") > -1) {
        return "Firefox";
    } //判断是否Firefox浏览器
    if (userAgent.indexOf("Chrome") > -1) {
        return "Chrome";
    }
    if (userAgent.indexOf("Safari") > -1) {
        return "Safari";
    } //判断是否Safari浏览器
    if (userAgent.indexOf("compatible") > -1 && userAgent.indexOf("MSIE") > -1 && !isOpera) {
        return "IE";//判断是否IE浏览器
    }
}

function changeStylesheet(stylesheetName, selectorText, ruleName, ruleValue){
    /*
    *
    * 更改样式表的规则
    *
    * stylesheetName：要修改的css文件名称（link标签里怎么引用的就写什么）;
    * selectorText：选择器文本
    * ruleName：要更改的规则名
    * ruleValue：要更改的规则值
    * */

    let styleSheets = document.styleSheets

    let stylesheet = null;

    for (let i = 0; i < styleSheets.length; i++) {
        // console.log(i)
        // console.log(styleSheets[i])
        const href = styleSheets[i].href
        if (href === null){
            continue;
        }
        // console.log(href, typeof(href));
        // console.log(href, typeof(href));
        if (href.indexOf(stylesheetName) !== -1){
            stylesheet = styleSheets[i];
        }
    }

    let elementRules;

    // looping through all its rules and getting your rule
    for(let i = 0; i < stylesheet.cssRules.length; i++) {
        // console.log(stylesheet.cssRules[i].selectorText)
        if(stylesheet.cssRules[i].selectorText === selectorText) {
            elementRules = stylesheet.cssRules[i];
        }
    }

    // modifying the rule in the stylesheet
    console.log(elementRules)
    elementRules.style.setProperty(ruleName, ruleValue);
}

window.onload = function (){
    if (webSort() === "Firefox") {
        console.log("是FireFox浏览器,启用浏览器调试")
        let color = "#31363b"

        changeStylesheet(
            "theme.css",
            '.cm-s-dracula.CodeMirror',
            'background-color',
            color);
    }
    /*Python留有的接口，通过它调用Python函数*/
    new QWebChannel(qt.webChannelTransport, function(channel) {
        PythonBridge = channel.objects.Bridge  // 获取Qt注册的对象
        PythonBridge.loadFinish();
    });
}

/* 给Python提供的方法 */

function changeTheme(stylesheetFile){
    /*
    * 更改theme
    * stylesheetFile: css文件路径
    * */
    function removeStyles (file) {
        let filename = file;
        let targetelement = "link";
        let targetattr = "href";
        let allsuspects = document.getElementsByTagName(targetelement);
        for (let i = allsuspects.length; i >= 0; i--) {
            if (allsuspects[i] && allsuspects[i].getAttribute(targetattr) != null && allsuspects[i].getAttribute(
                targetattr).indexOf(filename) !== -1) {
                allsuspects[i].parentNode.removeChild(allsuspects[i]);
            }
        }
    }
    function loadStyles (file) {
        let headElm = document.getElementsByTagName("head")[0];
        let fileref = document.createElement("link");
        fileref.setAttribute("rel", "stylesheet");
        fileref.setAttribute("type", "text/css");
        fileref.setAttribute("href", file);
        headElm.appendChild(fileref);
    }
    //
    removeStyles(stylesheetFile)
    loadStyles(stylesheetFile)
}

//设置编辑器内容
function setContent(connect){
    editor.doc.setValue(connect.data);
}

//插入内容
function insertContent(content){
    editor.replaceSelection(content.data)
}

// 运行命令
function execCommand(command){
    editor.execCommand(command.data);
}

function getSelection(){
    return editor.getSelection()
}

//更新主题
function updateTheme(){
    changeTheme("editor/css/theme.css")
}

function replaceSelection(data){
    let content = data.data
    editor.replaceSelection(content)
}

//编辑器内容改变信号
editor.on("change", function(mc) {
    // console.log(mc.doc.getValue());
    // 把内容交给子线程解析
    let content = mc.doc.getValue()
    PythonBridge.contentChange(content);
    let {undo, redo} = editor.historySize()
    console.log(undo, redo);

    PythonBridge.historySizeChange(JSON.stringify([undo, redo]))
    // console.log(editor.historySize())
});

editor.on("cursorActivity", (mc)=>{
    PythonBridge.selectionsChange(JSON.stringify(editor.getSelections()))
})

