#coding=utf-8
from flask import Flask,url_for,render_template,render_template_string,request
import urllib
import urllib2
import json

app = Flask(__name__)
initURL = "https://www.googleapis.com/customsearch/v1?key=AIzaSyCysqfXYhqcf8ITc-AJqISiSm740TsouYk&cx=009162889029278919880:2pcmrnqpomg"

@app.route('/')
def root():
    st = url_for('static', filename='google.png')
    jqsrc = url_for('static', filename='jquery.js')
    return render_template('index.html', imgst=st,jquerysrc=jqsrc)

@app.route('/sch',methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        s = request.form['q']
        src = s[::-1]
        sidx = request.form['start']    
    elif request.method == 'GET':
        s = request.args.get('q', '')
        src = s[::-1]
        sidx = request.args.get('start','1')
    squery = {"key":"AIzaSyCysqfXYhqcf8ITc-AJqISiSm740TsouYk","cx":"009162889029278919880:2pcmrnqpomg","q":src,"start":sidx}
    qurl = "https://www.googleapis.com/customsearch/v1?" + urllib.urlencode(squery)
    req=urllib2.Request(qurl,None,{'Referer':'http://Afflatusmind.com'})
    resp=urllib2.urlopen(req)
    jsondata=json.load(resp)    
    return genHTMLfromJSON(jsondata,s,sidx)

    
def genHTMLfromJSON(jsondata,q,sidx):
    first_page = """
                    <html>
                    <head>
                        <title>Fucking the GFW</title>
                        <script language="javascript" type="text/javascript" src="./static/jquery.js"></script>                        
                        <script language="javascript" type="text/javascript">
                        function verify() {
                            var key=document.sch.q.value;
                            if (key=="") {
                                alert("empty!");
                                return false;
                            }
                            else {                            
                                document.sch.q.value = key.split("").reverse().join("");            
                                return true;
                            }
                        }
                        </script>
                    </head>
                    <body>
                    <p>
                        <form id="sch" name="sch" method="post" action="./sch" onsubmit="return verify();">
                            <input id="sidx" name="start" type="hidden" value="1"/>
                            <input id="q" name="q" type="text" style="width:418px;" value="" />
                            <input id="su" name="su" type="submit"  value="Google it"/>
                        </form>
                    </p>
                    <p>
                        <div id="page">
                            {% for item in items %} 
                            <p>
                            <a href="{{ item.link }}" target="_blank">{{ item.title }}</a>
                            <br/><br/>{{item.snippet}}
                            </p>
                            {% endfor %} 
                            
                        </div>
                    </p>
                    <p align="center">
                        <div id="nextpage"><a href="./sch?q={{q}}&start={{nextstart}}">next page</a></div>
                    </p>
                    </body>
                    </html>
                """
    second_page = """
                    <p>
                        <form id="sch" name="sch" method="post" action="./sch">
                            <input id="sidx" name="start" type="hidden" value="1"/>
                            <input id="q" name="q" type="text" style="width:418px;" value="" />
                            <input id="su" name="su" type="submit"  value="Google it"/>
                        </form>
                    </p>
                    <div id="page">
                        {% for item in items %} 
                            <p>
                            <a href="{{ item.link }}" target="_blank">{{ item.title }}</a>
                            <br/><br/>{{item.snippet}}
                            </p>
                        {% endfor %} 
                    </div>
                    <p align="center">
                        <div id="nextpage"><a href="./sch?q={{q}}&start={{nextstart}}">next page</a></div>
                    </p>
                """
    if sidx=="1":
        #render with head script
        nextstart=jsondata["queries"]["nextPage"][0]["startIndex"]
        items = jsondata["items"]
        return render_template_string(first_page,items=items,q=q,nextstart=nextstart)
    else:
        #render without script
        nextstart=jsondata["queries"]["nextPage"][0]["startIndex"]
        items = jsondata["items"]
        return render_template_string(second_page,items=items,q=q,nextstart=nextstart)

if __name__ == '__main__':
    app.run(debug=True)