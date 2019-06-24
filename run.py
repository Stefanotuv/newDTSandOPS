__author__ = "stefanotuv"

from DTSandOPS import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True,use_reloader=True)
