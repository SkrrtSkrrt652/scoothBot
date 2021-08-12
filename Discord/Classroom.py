class Attendance:
    def __init__(self):
        self.classroom_vc = None
        self.track_text_attendance = 0
        self.track_voice_attendance = 0
        self.attendanceMsg = None
        self.attendees = set()
        # A dictionary with member as key and list [total time attended,
        # time of last entry into vc]
        self.vc_attendance = dict()

    def reset(self):
        self.track_text_attendance = 0
        self.track_voice_attendance = 0
        self.attendanceMsg = None
        self.attendees = set()
        self.vc_attendance = dict()


class PopQuiz:
    def __init__(self):
        self.optionEmojis = "🔵🔴🟢🟡⚪⚫🟣🟤"
        self.questions = []
        self.answers = dict()
        self.quizMessage = None
        self.current_qn = None
        self.thrown = 0
        self.total = 0
        self.correct = 0

    def parse(self, file):
        for line in file:
            print(line)
            parts = line.split(",")
            question = parts[0]
            ans_index = int(parts[-1])
            options = [option for option in parts[1:-1]]
            self.questions.append((question, tuple(options), ans_index))
