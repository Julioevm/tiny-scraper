import sys
import app

def main():
    
    path = sys.argv[1]
    app.start(path)

    while True:
        app.update()

if __name__ == "__main__":
    main()