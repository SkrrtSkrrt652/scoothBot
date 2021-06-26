class Attendance():
    def __init__(self):
        self.classroom_vcs = []
        self.text_attendance = 0
        self.voice_attendance = 0
        self.attendanceMsg = None
        self.attendees = set()
    
    def reset(self):
        self.text_attendance = 0
        self.voice_attendance = 0
        self.attendanceMsg = None
        self.attendees = set()
    