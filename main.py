import config_loader
import traceback
import baseobj
import time


def main() -> None:
    path = './config.json'
    print('Reading config ...')
    try:
        load = config_loader.load_config_file(path)
    except:
        info = traceback.format_exc()
        print(info, end='')
        input('Press enter to close the program...')
        return
    ctx = baseobj.RunningContext()
    if not load:
        return
    ctx.load_config(load)
    ctx.run()
    
    print('Load finish ...')
    
    try:
        while 1:
            time.sleep(0.5)
            if ctx.error_occured:
                input('Press enter to close the program...')
                break
    except KeyboardInterrupt:
        pass
    finally:
        ctx.end()
    
    while not ctx.thread_ended:
        time.sleep(0.1)
    
    print('Program end ...')
    
    return


if __name__ == '__main__':
    main()
