// 预览界面的js，主要负责解析markdown

filePath = "";

function resize() {
    let widgetWidth = document.documentElement.clientWidth;
    preview.setAttribute("style", "width:" + widgetWidth.toString() + "px;")
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

window.onload = function () {
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
    new QWebChannel(qt.webChannelTransport, function (channel) {
        PythonBridge = channel.objects.Bridge  // 获取Qt注册的对象
        initMarked();
        PythonBridge.loadFinish();
    });
}

function initMarked() {
    rendererMD = new marked.Renderer();
    // 重写heading，添加一个toc方法
    rendererMD.heading = function (text, level, raw) {
        console.log(text, level, raw)
        var anchor = tocObj.add(text, level);
        return `<a id=${anchor} class="anchor-fix"></a><h${level}>${text}</h${level}>\n`;
    };

    //处理网络链接，本地绝对链接，和相对链接
    rendererMD.image = function (href, title, text) {
        // return `<img src="http://127.0.0.1:5000?href=${href}" alt="${text}" title="${title ? title : ''}">`
        if(href.startsWith("http://")||href.startsWith("https://")) {
            return `<img src="${href}" class="markdown-img" alt="${text}" title="${title ? title : ''}">`
        }else if(href.startsWith("./")||href.startsWith("../")){
            return `<img src="file:///${filePath}/${href}" class="markdown-img" alt="${text}" title="${title ? title : ''}">`
        }else {

            /*
            * 这里应该添加相对引用的判断
            *  */

            return `<img src="file:///${href}" alt="${text}" class="markdown-img" title="${title ? title : ''}">`
        }
    }

    marked.setOptions({
        renderer: rendererMD,
        gfm: true,//它是一个布尔值，默认为true。允许 Git Hub标准的markdown.
        tables: true,//它是一个布尔值，默认为true。允许支持表格语法。该选项要求 gfm 为true。
        breaks: false,//它是一个布尔值，默认为false。允许回车换行。该选项要求 gfm 为true。
        pedantic: false,//它是一个布尔值，默认为false。尽可能地兼容 markdown.pl的晦涩部分。不纠正原始模型任何的不良行为和错误。
        sanitize: false,//它是一个布尔值，默认为false。对输出进行过滤（清理），将忽略任何已经输入的html代码（标签）
        smartLists: true,//它是一个布尔值，默认为false。使用比原生markdown更时髦的列表。 旧的列表将可能被作为pedantic的处理内容过滤掉.
        smartypants: false//它是一个布尔值，默认为false。使用更为时髦的标点，比如在引用语法中加入破折号。
    });

    // 结合mermaid语法
    marked.setOptions({
        highlight(code, type) {
            if (type === 'mermaid' || type === 'sequence' || type === 'flow') {
                return `<div class="mermaid">${code}</div>`;
            }
            return hljs.highlight(type, code).value;
            // return hljs.highlightAuto(code).value;
            //return hljs.highlight(code,code).value;
        }
    })
}

const tocObj = {
    add: function (text, level) {
        var anchor = `#toc${level}${++this.index}`;
        this.toc.push({anchor: anchor, level: level, text: text});
        return anchor;
    },
    // 使用堆栈的方式处理嵌套的ul,li，level即ul的嵌套层次，1是最外层
    // <ul>
    //   <li></li>
    //   <ul>
    //     <li></li>
    //   </ul>
    //   <li></li>
    // </ul>
    toHTML: function () {
        let levelStack = [];
        let result = '';
        const addStartUL = () => {
            result += '<ul>';
        };
        const addEndUL = () => {
            result += '</ul>\n';
        };
        const addLI = (anchor, text) => {
            result += '<li><a href="#' + anchor + '">' + text + '<a></li>\n';
        };

        this.toc.forEach(function (item) {
            let levelIndex = levelStack.indexOf(item.level);
            // 没有找到相应level的ul标签，则将li放入新增的ul中
            if (levelIndex === -1) {
                levelStack.unshift(item.level);
                addStartUL();
                addLI(item.anchor, item.text);
            } // 找到了相应level的ul标签，并且在栈顶的位置则直接将li放在此ul下
            else if (levelIndex === 0) {
                addLI(item.anchor, item.text);
            } // 找到了相应level的ul标签，但是不在栈顶位置，需要将之前的所有level出栈并且打上闭合标签，最后新增li
            else {
                while (levelIndex--) {
                    levelStack.shift();
                    addEndUL();
                }
                addLI(item.anchor, item.text);
            }
        });
        // 如果栈中还有level，全部出栈打上闭合标签
        while (levelStack.length) {
            levelStack.shift();
            addEndUL();
        }
        // 清理先前数据供下次使用
        this.toc = [];
        this.index = 0;
        return result;
    },
    toc: [],
    index: 0
};

/* 给Python提供的方法 */

function changeTheme(stylesheetFile) {
    /*
    * 更改theme
    * stylesheetFile: css文件路径
    * */
    function removeStyles(file) {
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

    function loadStyles(file) {
        let headElm = document.getElementsByTagName("head")[0];
        let fileref = document.createElement("link");
        fileref.setAttribute("rel", "stylesheet");
        fileref.setAttribute("type", "text/css");
        fileref.setAttribute("href", file);
        headElm.appendChild(fileref);
    }

    removeStyles(stylesheetFile)
    loadStyles(stylesheetFile)
}


function changePreviewTheme(oldStylesheetFile, newStylesheetFile) {
    /*
    * 更改预览界面的主题
    * stylesheetFile: css文件路径
    * */
    function removeStyles(file) {
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

    function loadStyles(file) {
        let headElm = document.getElementsByTagName("head")[0];
        let fileref = document.createElement("link");
        fileref.setAttribute("rel", "stylesheet");
        fileref.setAttribute("type", "text/css");
        fileref.setAttribute("href", file);
        headElm.appendChild(fileref);
    }

    removeStyles(oldStylesheetFile)
    loadStyles(newStylesheetFile)
}

//更新主题(其实没必要这里只是用了个滚动条的样式而已)
function updateTheme(){
    changeTheme("editor/css/theme.css")
}

// 更新预览主题
function updatePreviewTheme(data){
    console.log(data.data)
    changePreviewTheme(data.data[0], data.data[1])
}

function setFilePath(path){
    filePath = path.data;
}

function prase(content){
    // let data1 = new Date().getTime();
    content = marked(content.data);
    console.log(content)
    console.log(tocObj)
    tocHtml = "<div class='toc'><h3>文章目录</h3> " + tocObj.toHTML() + "</div>";
    content = content.replace(/<p>\[Toc]<\/p>/g,tocHtml);
    preview_inner.innerHTML = content;
    // let data3 = new Date().getTime();
    // console.log(data3-data1, data2-data1, data3-data2)  //总用时，解析用时，渲染用时
    return JSON.stringify({toc:tocHtml, previewHtml:content});
}


function skipTitle(data){
    location.href = data.data;
}
