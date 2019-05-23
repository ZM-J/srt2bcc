import os
import codecs
import json

def gettimenum(timestr):
    h, m, s = timestr.split(':')
    s, ms = s.split(',')
    h, m, s, ms = [int(_) for _ in [h, m, s, ms]]
    return h * 3600.0 + m * 60.0 + s + ms / 1000.0

def getbcc(subtitle_list):
    body = []
    body_json = {}
    state_str = 'find_index'
    for subtitle_str in subtitle_list:
        if (state_str == 'find_index'):
            state_str = 'find_times'
        elif (state_str == 'find_times'):
            times = subtitle_str
            start_time, end_time = times.split(' --> ')
            start_time = gettimenum(start_time)
            end_time = gettimenum(end_time)
            body_json['from'] = start_time
            body_json['to'] = end_time
            contents = []
            state_str = 'find_text'
        elif (state_str == 'find_text'):
            content = subtitle_str.strip()
            if (content == ''):
                contents = '\n'.join(contents)
                body_json['location'] = 2
                body_json['content'] = contents
                body.append(body_json)
                body_json = {}
                state_str = 'find_index'
            else:
                contents.append(content)
    bcc = {
        "font_size": 0.4,
        "font_color": "#FFFFFF",
        "background_alpha": 0.5,
        "background_color": "#9C27B0",
        "Stroke": "none",
        "body": body
    }
    return bcc

if __name__ == "__main__":
    srtdir = './srt'
    bccdir = './bcc'
    for fname in os.listdir(srtdir):
        with codecs.open(os.path.join(srtdir, fname), 'r', encoding='utf-8') as f:
            subtitle_list = f.readlines()
        bcc = getbcc(subtitle_list)
        name, _ = os.path.splitext(fname)
        bccname = name + '.bcc'
        with codecs.open(os.path.join(bccdir, bccname), 'w', encoding='utf-8') as f:
            json.dump(bcc, f, ensure_ascii=False)
