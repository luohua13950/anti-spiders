__author__ = 'luohua139'

class Common(object):

    @staticmethod
    def get_trace(slice_distance,append_end = True):
        start = 0
        trace = []
        if slice_distance < 70:
            accelerate_trace = 3 / 5 * slice_distance
        else:
            accelerate_trace = 4 / 5 * slice_distance
        s, v0, t = 0, 0, 0.1
        while start < slice_distance:
            if start < accelerate_trace:
                a = 1.2
            else:
                if slice_distance < 70:
                    a = -3
                else:
                    a = -5
            s = v0 * t + 1 / 2 * a * t ** 2
            v = v0 + a * t
            v0 = v
            start += s
            trace.append(round(s))
        if append_end:
            trace.append(1)
        print("轨迹和{}".format(sum(trace)))
        return trace