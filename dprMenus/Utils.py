import re
import mystic_bbs as bbs # pylint: disable=import-error


class Utils:
    @staticmethod
    def draw_box(y_height, color="|03"):
        flush_stdio = False
        try:
            build = int(bbs.mci2str("VR").split(' ')[1][1:])
            if build >= 46:
                flush_stdio = True
        except ValueError:
            pass
            
        vert_line = chr(179)
        top_rt = chr(191)
        top_lt = chr(218)
        bot_rt = chr(217)
        bot_lt = chr(192)
        line = chr(196)

        x_loc = 40
        y_loc = int((24- y_height)/2) - 1
        bbs.write(color)
        bbs.write("|[X"+str(x_loc).zfill(2) +"|[Y"+ str(y_loc).zfill(2) + top_lt + top_rt)
        for y in range(y_loc+1, y_loc+y_height+1):
            bbs.write("|[X"+str(x_loc).zfill(2) +"|[Y"+ str(y).zfill(2) + vert_line + vert_line)

        bbs.write("|[X"+str(x_loc).zfill(2) +"|[Y"+ str(y_loc+1+y_height).zfill(2) + bot_lt + bot_rt)
        if not flush_stdio:
            # To force it before delay bug
            bbs.write("|[X"+str(x_loc).zfill(2) +"|[Y"+ str(y_loc+1+y_height).zfill(2) + bot_lt + bot_rt)
        for i in range(0,38):
            if flush_stdio:
                bbs.flush()
            bbs.delay(10)
            bbs.write("|[X"+str(x_loc-i).zfill(2) +"|[Y"+ str(y_loc).zfill(2) + top_lt + line)
            bbs.write("|[X"+str(x_loc+i).zfill(2) +"|[Y"+ str(y_loc).zfill(2) + line + top_rt)
            for y in range(y_loc+1, y_loc+y_height+1):
                bbs.write("|[X"+str(x_loc-i).zfill(2) +"|[Y"+ str(y).zfill(2) + vert_line +  ' ')
                bbs.write("|[X"+str(x_loc + i).zfill(2) +"|[Y"+ str(y).zfill(2) + ' ' + vert_line)
            bbs.write("|[X"+str(x_loc-i).zfill(2) +"|[Y"+ str(y_loc+1+y_height).zfill(2) + bot_lt + line)
            bbs.write("|[X"+str(x_loc+i).zfill(2) +"|[Y"+ str(y_loc+1+y_height).zfill(2) + line + bot_rt)
            if not flush_stdio:
                # To force it before delay bug
                bbs.write("|[X"+str(x_loc+i).zfill(2) +"|[Y"+ str(y_loc+1+y_height).zfill(2) + line + bot_rt)
        if flush_stdio:
            bbs.flush()
        bbs.delay(50)
    
    # Virtual, override
    @staticmethod
    def writexy(x,y,string):
        bbs.write("|[X"+str(x).zfill(2)+"|[Y"+str(y).zfill(2)+str(string))

    # Virtual, override
    @staticmethod
    def reset_colors():
        bbs.write("|16|08")

    @staticmethod
    def strip_mci(string):
        # Strip only color and location codes so we can get an effective length
        rgx_list = [r'(\|\[[XY]\d{2})' , r'(\|\d{2})']
        new_text = string
        for rgx_match in rgx_list:
            new_text = re.sub(rgx_match, '', new_text)
        return new_text


