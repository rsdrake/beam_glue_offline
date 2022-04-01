# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = "Brett Feltmate & Richard Drake"

import klibs
from klibs                      import P
from klibs.KLAudio              import Tone
from klibs.KLUserInterface      import any_key, ui_request, key_pressed
from klibs.KLCommunication      import message
from klibs.KLGraphics           import KLDraw as kld
from klibs.KLGraphics           import fill, flip, blit
from klibs.KLResponseCollectors import RC_KEYPRESS, KeyPressResponse
from klibs.KLUtilities          import deg_to_px, hide_mouse_cursor, point_pos
from klibs.KLConstants          import TK_MS
from klibs.KLTime import Stopwatch

import random
import sdl2

# RGB constants for convenience
WHITE = [255, 255, 255, 255]
BLACK = [0,0,0,255]

class beam_glue(klibs.Experiment):


    def setup(self):
        self.colour_wheel = kld.ColorWheel(diameter=deg_to_px(20))

        green = self.colour_wheel.color_from_angle(120)
        blue = self.colour_wheel.color_from_angle(240)
        red = self.colour_wheel.color_from_angle(360)

        self.block_type = random.choice(['conjunction', 'feature'])

        # STIMULUS SIZES

        # fixation cross dimensions
        fixation_size =      deg_to_px(0.8)
        fixation_thickness = deg_to_px(0.1) # not sure... unspecified by Briand

        # arrow (cue) dimensions
        self.arrow_tail_len =     deg_to_px(0.4)
        self.arrow_tail_width =   deg_to_px(0.1)
        self.arrow_head_len =     deg_to_px(0.4)
        self.arrow_head_width =   deg_to_px(0.4, even=True)
        self.arrow_dimensions =   [self.arrow_tail_len, self.arrow_tail_width,
                                   self.arrow_head_len, self.arrow_head_width]



        # OFFSETS

        # distance between midpoint of letter stimuli and central fixation
        target_fixation_offset = deg_to_px(2)

        # should be 0.2 degrees between letters
        # therefore make them 0.1 degrees ± target_fixation_offset
        letter_offset = deg_to_px(0.1)

        # SET UP LOCATIONS (first, visual field Left or Right)
        self.left_vis = (P.screen_c[0] - target_fixation_offset, P.screen_c[1])
        self.right_vis = (P.screen_c[0] + target_fixation_offset, P.screen_c[1])

        # STIMULI
        # fixation cross
        self.fixation = kld.FixationCross(fixation_size, fixation_thickness, fill=WHITE)

        self.txtm.add_style(label="blue_text", color=blue)
        self.txtm.add_style(label="red_text", color=red)
        self.txtm.add_style(label="green_text", color=green)

        # letters themselves
        self.feature_targets = [
            ['O', 'blue_text'],
            ['T', 'blue_text'],
            ['X', 'blue_text'],
            ['O', 'red_text'],
            ['O', 'green_text']
        ]

        self.feature_distractors = [
            ['T', "red_text"],
            ['X', 'red_text'],
            ['T', 'green_text'],
            ['X', 'green_text']
        ]

        self.conjunction_targets = [
            ['O', 'blue_text']
        ]

        self.conjunction_distractors = [
            ['T', 'blue_text'],
            ['X', 'blue_text'],
            ['T', 'red_text'],
            ['O', 'red_text'],
            ['X', 'red_text'],
            ['O', 'green_text'],
            ['T', 'green_text'],
            ['X', 'green_text']
        ]

        # tone played after wrong keypress
        self.error_tone = Tone(500, 'sine', frequency=2000, volume=0.5)

        # Set up list of targets vs. distractors
        self.targets = self.feature_targets if self.block_type == 'feature' else self.conjunction_targets
        self.distractors = self.feature_distractors if self.block_type == 'feature' else self.conjunction_distractors

        keymap_a = {'/': 'present', 'z': 'absent'}
        keymap_b = {'/': 'absent', 'z': 'present'}

        self.keymap = random.choice([keymap_a, keymap_b])

        self.resume_txt = "{0}\n\nPress apostrophe (\') to start each trial and spacebar to continue..."
        #txt = theothertext.format(self.resume_txt)

        self.insert_practice_block(block_nums=1, trial_counts=25)
        self.insert_practice_block(block_nums=3, trial_counts=25)



    def block(self):
        if P.block_number == 1:

            if self.block_type == 'conjunction':
                self.instruction_txt = """In this block, you will see a group of letters.
You are looking for a blue letter O.
Please press '/' for target {0} and 'z' for target {1}.""".format(self.keymap['/'], self.keymap['z'])

            else:
                self.instruction_txt = """In this block, you will see a group of letters.
You are looking for the letter O or a blue letter.
Please press '/' for target {0} and 'z' for target {1}.""".format(self.keymap['/'], self.keymap['z'])

            #txt = "Please press '/' for target {0} and 'z' for target {1}".format(self.keymap['/'], self.keymap['z'])

            self.instruction_txt = self.resume_txt.format(self.instruction_txt)

            msg = message(self.instruction_txt, registration = 5, location = P.screen_c, align = 'center', blit_txt = False)

            # Because blit_txt = False above:
            fill()
            blit(msg, location = P.screen_c, registration = 5)
            flip()

            while True:
                ui_request() # added security
                if key_pressed(key = sdl2.SDLK_SPACE): # SDLK_SPACE not ergonomic
                    break


        if P.block_number == 3:

            self.block_type = 'conjunction' if self.block_type == 'feature' else 'feature'

            if self.block_type == 'conjunction':
                self.instruction_txt = """In this block, you will see a group of letters.
You are looking for a blue letter O.
Please press '/' for target {0} and 'z' for target {1}.""".format(self.keymap['/'], self.keymap['z'])

            else:
                self.instruction_txt = """In this block, you will see a group of letters.
You are looking for the letter O or a blue letter.
Please press '/' for target {0} and 'z' for target {1}.""".format(self.keymap['/'], self.keymap['z'])

            self.instruction_txt = self.resume_txt.format(self.instruction_txt)

            msg = message(self.instruction_txt, registration = 5, location = P.screen_c, align = 'center', blit_txt = False)

            # Because blit_txt = False above:
            fill()
            blit(msg, location = P.screen_c, registration = 5)
            flip()

            while True:
                ui_request() # added security
                if key_pressed(key = sdl2.SDLK_SPACE): # SDLK_SPACE not ergonomic
                    break

            self.targets = self.feature_targets if self.block_type == 'feature' else self.conjunction_targets
            self.distractors = self.feature_distractors if self.block_type == 'feature' else self.conjunction_distractors

    def setup_response_collector(self):
        self.rc.uses(RC_KEYPRESS) # this creates a class called keypress_listener in the background
        self.rc.keypress_listener.key_map = self.keymap
        self.rc.terminate_after = [9999, TK_MS]
        self.rc.keypress_listener.interrupts = True
        self.rc.display_callback = self.rc_callback

    def trial_prep(self):

        # break during block... otherwise add the message and anykey lines to block(self)
        if P.trial_number == P.trials_per_block / 2:
            message("Take a break. Press apostrophe (\') when you are ready.", location = P.screen_c, blit_txt = True)
            while True:
                if key_pressed(key = sdl2.SDLK_QUOTE): # SDLK_SPACE not ergonomic
                    break

        if self.cue_valid:
            rotation = 180 if self.visual_field == 'left' else 0
            self.cue_direction = 'left' if self.visual_field == 'left' else 'right'
        else:
            rotation = 0 if self.visual_field == 'left' else 180
            self.cue_direction = 'right' if self.visual_field == 'left' else 'left'

        self.arrow = kld.Arrow(*self.arrow_dimensions, rotation = rotation, fill=WHITE)

        if P.condition == '2':
            if self.visual_field == 'left':
                self.array_locs = [
                    point_pos(self.left_vis, deg_to_px(0.4), angle=180),
                    point_pos(self.left_vis, deg_to_px(0.4), angle=360)
                ]
            else:
                self.array_locs = [
                    point_pos(self.right_vis, deg_to_px(0.4), angle=180),
                    point_pos(self.right_vis, deg_to_px(0.4), angle=360)
                ]
        else:
            if self.visual_field == 'left':
                self.array_locs = [
                    point_pos(self.left_vis, deg_to_px(0.7), angle=45),
                    point_pos(self.left_vis, deg_to_px(0.7), angle=135),
                    point_pos(self.left_vis, deg_to_px(0.7), angle=225),
                    point_pos(self.left_vis, deg_to_px(0.7), angle=315)
                ]
            else:
                self.array_locs = [
                    point_pos(self.right_vis, deg_to_px(0.7), angle=45),
                    point_pos(self.right_vis, deg_to_px(0.7), angle=135),
                    point_pos(self.right_vis, deg_to_px(0.7), angle=225),
                    point_pos(self.right_vis, deg_to_px(0.7), angle=315)
                ]

        random.shuffle(self.array_locs)

        self.display_items = []  # stimuli to display

        if self.target_present:
            if P.condition == '2':
                # construction where Python knows to assign both an id and a colour
                self.target_id, self.target_col = random.choice(self.targets)  # python should be able to cope with this construction
                self.distractor_id, self.distractor_col = random.choice(self.distractors)

                self.display_items = {
                    0: message(self.target_id, style=self.target_col, blit_txt=False, align='center'),
                    1: message(self.distractor_id, style=self.distractor_col, blit_txt=False, align='center')
                }

            else:  # if P.condition == 4
                self.target_id, self.target_col = random.choice(self.targets)
                distractors_dummy = random.sample(self.distractors, 3)

                self.distractor1_id, self.distractor1_col = distractors_dummy[0]
                self.distractor2_id, self.distractor2_col = distractors_dummy[1]
                self.distractor3_id, self.distractor3_col = distractors_dummy[2]

                self.display_items = {
                    0: message(self.target_id, style=self.target_col, blit_txt=False, align='center'),
                    1: message(self.distractor1_id, style=self.distractor1_col, blit_txt=False, align='center'),
                    2: message(self.distractor2_id, style=self.distractor2_col, blit_txt=False, align='center'),
                    3: message(self.distractor3_id, style=self.distractor3_col, blit_txt=False, align='center')
                }

        else:  # if target absent
            if P.condition == '2':
                distractors_dummy = random.sample(self.distractors, 2)
                self.distractor1_id, self.distractor1_col = distractors_dummy[0]
                self.distractor2_id, self.distractor2_col = distractors_dummy[1]

                self.display_items = {
                    0: message(self.distractor1_id, style=self.distractor1_col, blit_txt=False, align='center'),
                    1: message(self.distractor2_id, style=self.distractor2_col, blit_txt=False, align='center')
                }

            else:
                distractors_dummy = random.sample(self.distractors, 4)
                self.distractor1_id, self.distractor1_col = distractors_dummy[0]
                self.distractor2_id, self.distractor2_col = distractors_dummy[1]
                self.distractor3_id, self.distractor3_col = distractors_dummy[2]
                self.distractor4_id, self.distractor4_col = distractors_dummy[3]

                self.display_items = {
                    0: message(self.distractor1_id, style=self.distractor1_col, blit_txt=False, align='center'),
                    1: message(self.distractor2_id, style=self.distractor2_col, blit_txt=False, align='center'),
                    2: message(self.distractor3_id, style=self.distractor3_col, blit_txt=False, align='center'),
                    3: message(self.distractor4_id, style=self.distractor4_col, blit_txt=False, align='center')
                }

        # Establish sequence of events
        events = []
        events.append(['cue_onset', 800])
        events.append(['display_onset', events[-1][1] + 500]) # -1 for previous item, which is a list of 2 items. Want second item.
        events.append(['display_offset', events[-1][1] + 83.33])
        self.evm.register_tickets(events)

        # hide cursor during trial
        hide_mouse_cursor()

        self.trial_init()
        hide_mouse_cursor()

    def trial(self):

        while self.evm.before('cue_onset'):
            ui_request() # basically the same as pass but will continuously listen for input like 'quit'... there is also smart_sleep()

        self.present_arrow()

        while self.evm.before('display_onset'):
            ui_request()

        self.rc.collect()

        if len(self.rc.keypress_listener.response()):
            self.response, self.rt = self.rc.keypress_listener.response()

        else:
            self.response, self.rt = 'NA', 'NA'

        if self.target_present:
            if self.response != 'present':
                self.error = 1
                self.error_tone.play()
            else:
                self.error = 0

        else:
            if self.response != 'absent':
                self.error_tone.play()
                self.error = 1
            else:
                self.error = 0

        return {
            "block_num": P.block_number,
            "trial_num": P.trial_number,
            "practicing": str(P.practicing),
            "condition": P.condition,
            "block_type": self.block_type,
            "response": self.response,
            "rt": self.rt,
            "error": self.error,
            "cue_valid": str(self.cue_valid),
            "visual_field": self.visual_field,
            "cue_direction": self.cue_direction
        }

    def trial_clean_up(self):
        pass

    def clean_up(self):
        pass

    def trial_init(self):
        fill()
        blit(self.fixation, registration=5, location=P.screen_c)
        flip()

        # any_key() # this would be as opposed to using the space bar, which is given in the 3 lines below
        while True:
            if key_pressed(key = sdl2.SDLK_QUOTE): # SDLK_SPACE not ergonomic
                break

    def present_arrow(self):
        fill()
        blit(self.arrow, registration=5, location=P.screen_c)
        flip()

    def present_array(self):
        fill()
        blit(self.arrow, registration=5, location=P.screen_c)
        for i in range(int(P.condition)):
            blit(self.display_items[i], location=self.array_locs[i], registration=5)
        flip()


    def rc_callback(self):
        if self.evm.before('display_offset'):
            self.present_array()
        else:
            fill()
            flip()
