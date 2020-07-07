import re
import mystic_bbs as bbs # pylint: disable=import-error


class Utils:
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


