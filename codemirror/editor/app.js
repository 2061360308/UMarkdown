//中间spitter控件拖动，控制分割窗口大小
// 鼠标按下事件
splitter.onmousedown = (e) => {
    // console.log(e)
    // 获取鼠标初始位置x坐标
    e = e || window.event
    var o_clientX = e.clientX
    // 鼠标移动，更改编辑框和预览框位置
    document.onmousemove = (e) => {
        e = e || window.event
        //console.log(e.clientX-o_clientX);

        //console.log()
        //判断编辑器宽是否最小宽度
        let editor_new_w = editorElm.offsetWidth + e.clientX - o_clientX
        let preview_new_w = preview.offsetWidth - e.clientX + o_clientX
        var window_w = document.body.clientWidth;
        if (editor_new_w <= 0) {
            editorElm.setAttribute("style", "width:0px"); //编辑器最小宽
            //调整预览框以适应空余空间
            preview.setAttribute("style",
                "width:" + (window_w - splitter_w).toString() + "px;left:" + splitter_w.toString() + "px;");
            document.onmousemove = null
            splitter.setAttribute("style", "left:0")
        } else {
            if (editor_new_w < (window_w - splitter_w)) {
                editorElm.setAttribute("style", "width:" + editor_new_w.toString() + "px;");
                preview.setAttribute("style",
                    "width:" + preview_new_w.toString() + "px;" +
                    "left:" + (editor_new_w + splitter_w).toString() + "px;"
                )
                //splitter.style.left = (splitter.offsetX + e.clientX-o_clientX).toString() + "px";
                splitter.setAttribute("style", "left:" + editor_new_w.toString() + "px;")
            } else {
                editorElm.setAttribute("style", "width:" + (window_w - splitter_w).toString() + "px;");
                preview.setAttribute("style",
                    "width:0px;", +
                    "left:" + (window_w + splitter_w).toString() + "px;"
                );
                splitter.style.left = (window_w - splitter_w).toString() + "px";
                document.onmousemove = null
            }
        }

        o_clientX = e.clientX;
    }
}

// 鼠标松开
splitter.onmouseup = () => {
    document.onmousemove = null
    //editor.resize();
}
window.onresize = resize;

function resize() {
    let changeNum = document.documentElement.clientWidth - (editorElm.clientWidth + preview.clientWidth + splitter_w)
    let new_editor_w = editorElm.clientWidth + changeNum
    console.log(changeNum, new_editor_w)
    editorElm.setAttribute("style", "width:" + new_editor_w.toString() + "px;")
    splitter.setAttribute("style", "left:" + new_editor_w.toString() + "px;")
    preview.setAttribute("style", "left:" + (new_editor_w + splitter_w).toString() + "px;" +
        "width:" + (document.documentElement.clientWidth - (editorElm.clientWidth + splitter_w)).toString() + "px;")
    console.log('可视宽' + document.documentElement.clientWidth);
    console.log('可视高' + document.documentElement.clientHeight);
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

function changeStylesheet(stylesheetIndex, selectorText, ruleName, ruleValue){
    /*
    *
    * 更改样式表的规则
    *
    * stylesheetIndex：stylesheetIndex的索引，通过console.log(document.styleSheets);查看
    * selectorText：选择器文本
    * ruleName：要更改的规则名
    * ruleValue：要更改的规则值
    * */
    const stylesheet = document.styleSheets[stylesheetIndex];
    let elementRules;

    // looping through all its rules and getting your rule
    for(let i = 0; i < stylesheet.cssRules.length; i++) {
        // console.log(stylesheet.cssRules[i].selectorText)
        if(stylesheet.cssRules[i].selectorText === selectorText) {
            elementRules = stylesheet.cssRules[i];
        }
    }

    // modifying the rule in the stylesheet
    elementRules.style.setProperty(ruleName, ruleValue);
}

window.onload = function (){
    if (webSort() === "Firefox") {
        console.log("是FireFox浏览器,启用浏览器调试")
        let color = "#31363b"

        changeStylesheet(
            7,
            '.cm-s-dracula.CodeMirror, #preview, #splitter',
            'background-color',
            color);
    }
}

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

