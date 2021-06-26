class Attendance():
    def __init__(self):
        self.classroom_vc = None
        self.track_text_attendance = 0
        self.track_voice_attendance = 0
        self.attendanceMsg = None
        self.attendees = set()
        #A dictionary with member as key and list [total time attended, time of last entry into vc]
        self.vc_attendance = dict()
    
    def reset(self):
        self.track_text_attendance = 0
        self.track_voice_attendance = 0
        self.attendanceMsg = None
        self.attendees = set()
        self.vc_attendance = dict()
    


    