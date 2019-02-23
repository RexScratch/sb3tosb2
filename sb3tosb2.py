import sys, json, zipfile
sys.setrecursionlimit(4100)

def printWarning(message):
    print("WARNING: " + message)

def printError(message):
    lines = message.split('\n')
    lines = ["       " + line for line in lines]
    lines[0] = "ERROR: " + lines[0][7:]
    print('\n'.join(lines))
    exit()

class BlockArgMapper:

    def __init__(self, obj):
        assert type(obj) == ProjectConverter
        self.converter = obj

    def mapArgs(self, opcode, block, blocks):
        assert not opcode.startswith('__')
        return getattr(self, opcode)(block, blocks)

    # Motion

    def motion_movesteps(self, block, blocks):
        output = ['forward:']
        output.append(self.converter.inputVal('STEPS', block, blocks))
        return output

    def motion_turnright(self, block, blocks):
        output = ['turnRight:']
        output.append(self.converter.inputVal('DEGREES', block, blocks))
        return output

    def motion_turnleft(self, block, blocks):
        output = ['turnLeft:']
        output.append(self.converter.inputVal('DEGREES', block, blocks))
        return output

    def motion_pointindirection(self, block, blocks):
        output = ['heading:']
        output.append(self.converter.inputVal('DIRECTION', block, blocks))
        return output

    def motion_pointtowards(self, block, blocks):
        output = ['pointTowards:']
        output.append(self.converter.inputVal('TOWARDS', block, blocks))
        return output

    def motion_gotoxy(self, block, blocks):
        output = ['gotoX:y:']
        output.append(self.converter.inputVal('X', block, blocks))
        output.append(self.converter.inputVal('Y', block, blocks))
        return output

    def motion_goto(self, block, blocks):
        output = ['gotoSpriteOrMouse:']
        output.append(self.converter.inputVal('TO', block, blocks))
        return output

    def motion_glidesecstoxy(self, block, blocks):
        output = ['glideSecs:toX:y:elapsed:from:']
        output.append(self.converter.inputVal('SECS', block, blocks))
        output.append(self.converter.inputVal('X', block, blocks))
        output.append(self.converter.inputVal('Y', block, blocks))
        return output

    def motion_changexby(self, block, blocks):
        output = ['changeXposBy:']
        output.append(self.converter.inputVal('DX', block, blocks))
        return output

    def motion_setx(self, block, blocks):
        output = ['xpos:']
        output.append(self.converter.inputVal('X', block, blocks))
        return output

    def motion_changeyby(self, block, blocks):
        output = ['changeYposBy:']
        output.append(self.converter.inputVal('DY', block, blocks))
        return output

    def motion_sety(self, block, blocks):
        output = ['ypos:']
        output.append(self.converter.inputVal('Y', block, blocks))
        return output

    def motion_ifonedgebounce(self, block, blocks):
        return ['bounceOffEdge']

    def motion_setrotationstyle(self, block, blocks):
        output = ['setRotationStyle']
        output.append(self.converter.fieldVal('STYLE', block))
        return output

    def motion_xposition(self, block, blocks):
        return ['xpos']

    def motion_yposition(self, block, blocks):
        return ['ypos']

    def motion_direction(self, block, blocks):
        return ['heading']

    def motion_scroll_right(self, block, blocks):
        output = ['scrollRight']
        output.append(self.converter.inputVal('DISTANCE', block, blocks))
        return output
    
    def motion_scroll_up(self, block, blocks):
        output = ['scrollUp']
        output.append(self.converter.inputVal('DISTANCE', block, blocks))
        return output

    def motion_align_scene(self, block, blocks):
        output = ['scrollAlign']
        output.append(self.converter.fieldVal('ALIGNMENT', block))
        return output

    def motion_xscroll(self, block, blocks):
        return ['xScroll']

    def motion_yscroll(self, block, blocks):
        return ['yScroll']
    
    # Looks

    def looks_sayforsecs(self, block, blocks):
        output = ['say:duration:elapsed:from:']
        output.append(self.converter.inputVal('MESSAGE', block, blocks))
        output.append(self.converter.inputVal('SECS', block, blocks))
        return output

    def looks_say(self, block, blocks):
        output = ['say:']
        output.append(self.converter.inputVal('MESSAGE', block, blocks))
        return output

    def looks_thinkforsecs(self, block, blocks):
        output = ['think:duration:elapsed:from:']
        output.append(self.converter.inputVal('MESSAGE', block, blocks))
        output.append(self.converter.inputVal('SECS', block, blocks))
        return output

    def looks_think(self, block, blocks):
        output = ['think:']
        output.append(self.converter.inputVal('MESSAGE', block, blocks))
        return output

    def looks_show(self, block, blocks):
        return ['show']

    def looks_hide(self, block, blocks):
        return ['hide']

    def looks_hideallsprites(self, block, blocks):
        return ['hideAll']

    def looks_switchcostumeto(self, block, blocks):
        output = ['lookLike:']
        output.append(self.converter.inputVal('COSTUME', block, blocks))
        return output

    def looks_nextcostume(self, block, blocks):
        return ['nextCostume']
    
    def looks_switchbackdropto(self, block, blocks):
        output = ['startScene']
        output.append(self.converter.inputVal('BACKDROP', block, blocks))
        return output

    def looks_changeeffectby(self, block, blocks):
        output = ['changeGraphicEffect:by:']
        field = self.converter.fieldVal('EFFECT', block)
        if type(field) == str:
            field = str.lower(field)
        output.append(field)
        output.append(self.converter.inputVal('CHANGE', block, blocks))
        return output

    def looks_seteffectto(self, block, blocks):
        output = ['setGraphicEffect:to:']
        field = self.converter.fieldVal('EFFECT', block)
        if type(field) == str:
            field = str.lower(field)
        output.append(field)
        output.append(self.converter.inputVal('VALUE', block, blocks))
        return output
    
    def looks_cleargraphiceffects(self, block, blocks):
        return ['filterReset']

    def looks_changesizeby(self, block, blocks):
        output = ['changeSizeBy:']
        output.append(self.converter.inputVal('CHANGE', block, blocks))
        return output

    def looks_setsizeto(self, block, blocks):
        output = ['setSizeTo:']
        output.append(self.converter.inputVal('SIZE', block, blocks))
        return output

    def looks_changestretchby(self, block, blocks):
        output = ['changeStretchBy:']
        output.append(self.converter.inputVal('CHANGE', block, blocks))
        return output

    def looks_setstretchto(self, block, blocks):
        output = ['setStretchTo:']
        output.append(self.converter.inputVal('STRETCH', block, blocks))
        return output

    def looks_gotofrontback(self, block, blocks):
        field = self.converter.fieldVal('FRONT_BACK', block)
        if field == 'front':
            return ['comeToFront']
        else:
            self.converter.generateWarning("Incompatible block 'go to [back v] layer' will be converted to 'go back (1.79e+308) layers'")
            return ['goBackByLayers:', 1.79e+308]

    def looks_goforwardbackwardlayers(self, block, blocks):
        layers = self.converter.inputVal('NUM', block, blocks)
        field = self.converter.fieldVal('FORWARD', block)
        if field == 'forward':
            if type(layers) == str:
                try:
                    layers = float(layers)
                except:
                    pass
            if type(layers) == float or type(layers) == int:
                layers *= -1
            else:
                layers = ['*', -1, layers]
        return ['goBackByLayers:', layers]

    def looks_costumenumbername(self, block, blocks):
        field = self.converter.fieldVal('NUMBER_NAME', block)
        if field == 'number':
            return ['costumeIndex']
        elif field == 'name':
            self.converter.generateWarning("Incompatible block 'costume [name v]")
            return ['costumeName']

    def looks_backdropnumbername(self, block, blocks):
        field = self.converter.fieldVal('NUMBER_NAME', block)
        if field == 'number':
            return ['backgroundIndex']
        elif field == 'name':
            return ['sceneName']

    def looks_size(self, block, blocks):
        return ['scale']

    def looks_switchbackdroptoandwait(self, block, blocks):
        output = ['startSceneAndWait']
        output.append(self.converter.inputVal('BACKDROP', block, blocks))
        return output

    def looks_nextbackdrop(self, block, blocks):
        return ['nextScene']

    # Sound

    def sound_play(self, block, blocks):
        output = ['playSound:']
        output.append(self.converter.inputVal('SOUND_MENU', block, blocks))
        return output
    
    def sound_playuntildone(self, block, blocks):
        output = ['doPlaySoundAndWait']
        output.append(self.converter.inputVal('SOUND_MENU', block, blocks))
        return output

    def sound_stopallsounds(self, block, blocks):
        return ['stopAllSounds']
    
    def sound_changevolumeby(self, block, blocks):
        output = ['changeVolumeBy:']
        output.append(self.converter.inputVal('VOLUME', block, blocks))
        return output

    def sound_setvolumeto(self, block, blocks):
        output = ['setVolumeTo:']
        output.append(self.converter.inputVal('VOLUME', block, blocks))
        return output

    def sound_volume(self, block, blocks):
        return ['volume']

    # Music

    def music_playDrumForBeats(self, block, blocks):
        output = ['playDrum']
        output.append(self.converter.inputVal('DRUM', block, blocks))
        output.append(self.converter.inputVal('BEATS', block, blocks))
        return output

    def music_midiPlayDrumForBeats(self, block, blocks):
        output = ['drum:duration:elapsed:from:']
        output.append(self.converter.inputVal('DRUM', block, blocks))
        output.append(self.converter.inputVal('BEATS', block, blocks))
        return output

    def music_restForBeats(self, block, blocks):
        output = ['rest:elapsed:from:']
        output.append(self.converter.inputVal('BEATS', block, blocks))
        return output

    def music_playNoteForBeats(self, block, blocks):
        output = ['noteOn:duration:elapsed:from:']
        output.append(self.converter.inputVal('NOTE', block, blocks))
        output.append(self.converter.inputVal('BEATS', block, blocks))
        return output

    def music_setInstrument(self, block, blocks):
        output = ['instrument:']
        output.append(self.converter.inputVal('INSTRUMENT', block, blocks))
        return output

    def music_midiSetInstrument(self, block, blocks):
        output = ['midiInstrument:']
        output.append(self.converter.inputVal('INSTRUMENT', block, blocks))
        return output

    def music_changeTempo(self, block, blocks):
        output = ['changeTempoBy:']
        output.append(self.converter.inputVal('TEMPO', block, blocks))
        return output

    def music_setTempo(self, block, blocks):
        output = ['setTempoTo:']
        output.append(self.converter.inputVal('TEMPO', block, blocks))
        return output

    def music_getTempo(self, block, blocks):
        return ['tempo']

    # Pen

    def pen_clear(self, block, blocks):
        return ['clearPenTrails']

    def pen_stamp(self, block, blocks):
        return ['stampCostume']

    def pen_penDown(self, block, blocks):
        return ['putPenDown']

    def pen_penUp(self, block, blocks):
        return ['putPenUp']

    def pen_setPenColorToColor(self, block, blocks):
        output = ['penColor:']
        output.append(self.converter.inputVal('COLOR', block, blocks))
        return output

    def pen_changePenHueBy(self, block, blocks):
        output = ['changePenHueBy:']
        output.append(self.converter.inputVal('HUE', block, blocks))
        return output

    def pen_setPenHueToNumber(self, block, blocks):
        output = ['setPenHueTo:']
        output.append(self.converter.inputVal('HUE', block, blocks))
        return output

    def pen_changePenShadeBy(self, block, blocks):
        output = ['changePenShadeBy:']
        output.append(self.converter.inputVal('SHADE', block, blocks))
        return output

    def pen_setPenShadeToNumber(self, block, blocks):
        output = ['setPenShadeTo:']
        output.append(self.converter.inputVal('SHADE', block, blocks))
        return output

    def pen_changePenSizeBy(self, block, blocks):
        output = ['changePenSizeBy:']
        output.append(self.converter.inputVal('SIZE', block, blocks))
        return output

    def pen_setPenSizeTo(self, block, blocks):
        output = ['penSize:']
        output.append(self.converter.inputVal('SIZE', block, blocks))
        return output

    def pen_setPenColorParamTo(self, block, blocks):
        param = self.converter.inputVal('COLOR_PARAM', block, blocks)
        value = self.converter.inputVal('VALUE', block, blocks)
        if param == 'color':
            output = ['setPenHueTo:']
            output.append(value)
            return output
        elif param == 'brightness':
            if type(value) == str:
                try:
                    value = float(value)
                except:
                    pass
            if type(value) == float or type(value) == int:
                value /= 2
            else:
                value = ['/', value, 2]
            output = ['setPenShadeTo:']
            output.append(value)
            return output
        else:
            self.converter.generateWarning("Incompatible block 'set pen [{} v] to ({})'".format(param, value))
            return ['pen_setPenColorParamTo', value, param]

    def pen_changePenColorParamBy(self, block, blocks):
        param = self.converter.inputVal('COLOR_PARAM', block, blocks)
        value = self.converter.inputVal('VALUE', block, blocks)
        if param == 'color':
            output = ['changePenHueBy:']
            output.append(value)
            return output
        elif param == 'brightness':
            if type(value) == str:
                try:
                    value = float(value)
                except:
                    pass
            if type(value) == float or type(value) == int:
                value /= 2
            else:
                value = ['/', value, 2]
            output = ['changePenShadeBy:']
            output.append(value)
            return output
        else:
            self.converter.generateWarning("Incompatible block 'change pen [{} v] by ({})'".format(param, value))
            return ['pen_changeColorParamBy', value, param]

    # Events

    def event_whenflagclicked(self, block, blocks):
        return ['whenGreenFlag']

    def event_whenkeypressed(self, block, blocks):
        output = ['whenKeyPressed']
        output.append(self.converter.fieldVal('KEY_OPTION', block))
        return output

    def event_whenthisspriteclicked(self, block, blocks):
        return ['whenClicked']

    def event_whenbackdropswitchesto(self, block, blocks):
        output = ['whenSceneStarts']
        output.append(self.converter.fieldVal('BACKDROP', block))
        return output

    def event_whengreaterthan(self, block, blocks):
        output = ['whenSensorGreaterThan']
        field = self.converter.fieldVal('WHENGREATERTHANMENU', block)
        if type(field) == str:
            field = str.lower(field)
        output.append(field)
        output.append(self.converter.inputVal('VALUE', block, blocks))
        return output
    
    def event_whenbroadcastreceived(self, block, blocks):
        output = ['whenIReceive']
        output.append(self.converter.fieldVal('BROADCAST_OPTION', block))
        return output
    
    def event_broadcast(self, block, blocks):
        output = ['broadcast:']
        output.append(self.converter.inputVal('BROADCAST_INPUT', block, blocks))
        return output

    def event_broadcastandwait(self, block, blocks):
        output = ['doBroadcastAndWait']
        output.append(self.converter.inputVal('BROADCAST_INPUT', block, blocks))
        return output

    # Control

    def control_wait(self, block, blocks):
        output = ['wait:elapsed:from:']
        output.append(self.converter.inputVal('DURATION', block, blocks))
        return output
    
    def control_repeat(self, block, blocks):
        output = ['doRepeat']
        output.append(self.converter.inputVal('TIMES', block, blocks))
        output.append(self.converter.substackVal('SUBSTACK', block, blocks))
        return output
    
    def control_forever(self, block, blocks):
        output = ['doForever']
        output.append(self.converter.substackVal('SUBSTACK', block, blocks))
        return output
    
    def control_if(self, block, blocks):
        output = ['doIf']
        output.append(self.converter.inputVal('CONDITION', block, blocks))
        output.append(self.converter.substackVal('SUBSTACK', block, blocks))
        return output

    def control_if_else(self, block, blocks):
        output = ['doIfElse']
        output.append(self.converter.inputVal('CONDITION', block, blocks))
        output.append(self.converter.substackVal('SUBSTACK', block, blocks))
        output.append(self.converter.substackVal('SUBSTACK2', block, blocks))
        return output

    def control_wait_until(self, block, blocks):
        output = ['doWaitUntil']
        output.append(self.converter.inputVal('CONDITION', block, blocks))
        return output

    def control_repeat_until(self, block, blocks):
        output = ['doUntil']
        output.append(self.converter.inputVal('CONDITION', block, blocks))
        output.append(self.converter.substackVal('SUBSTACK', block, blocks))
        return output

    def control_while(self, block, blocks):
        output = ['doWhile']
        output.append(self.converter.inputVal('CONDITION', block, blocks))
        output.append(self.converter.substackVal('SUBSTACK', block, blocks))
        return output

    def control_for_each(self, block, blocks):
        output = ['doForLoop']
        output.append(self.converter.fieldVal('VARIABLE', block))
        output.append(self.converter.inputVal('VALUE', block, blocks))
        output.append(self.converter.substackVal('SUBSTACK', block, blocks))
        return output
    
    def control_stop(self, block, blocks):
        output = ['stopScripts']
        output.append(self.converter.fieldVal('STOP_OPTION', block))
        return output
    
    def control_start_as_clone(self, block, blocks):
        return ['whenCloned']

    def control_create_clone_of(self, block, blocks):
        output = ['createCloneOf']
        output.append(self.converter.inputVal('CLONE_OPTION', block, blocks))
        return output
    
    def control_delete_this_clone(self, block, blocks):
        return ['deleteClone']

    def control_get_counter(self, block, blocks):
        return ['COUNT']

    def control_incr_counter(self, block, blocks):
        return ['INCR_COUNT']

    def control_clear_counter(self, block, blocks):
        return ['CLR_COUNT']

    def control_all_at_once(self, block, blocks):
        output = ['warpSpeed']
        output.append(self.converter.substackVal('SUBSTACK', block, blocks))
        return output

    # Video Sensing

    def videoSensing_videoOn(self, block, blocks):
        output = ['senseVideoMotion']
        output.append(self.converter.inputVal('ATTRIBUTE', block, blocks))
        output.append(self.converter.inputVal('SUBJECT', block, blocks))
        return output

    def videoSensing_whenMotionGreaterThan(self, block, blocks):
        output = ['whenSensorGreaterThan', 'video motion']
        output.append(self.converter.inputVal('REFERENCE', block, blocks))
        return output

    def videoSensing_videoToggle(self, block, blocks):
        output = ['setVideoState']
        output.append(self.converter.inputVal('VIDEO_STATE', block, blocks))
        return output

    def videoSensing_setVideoTransparency(self, block, blocks):
        output = ['setVideoTransparency']
        output.append(self.converter.inputVal('TRANSPARENCY', block, blocks))
        return output

    # Sensing

    def sensing_touchingobject(self, block, blocks):
        output = ['touching:']
        output.append(self.converter.inputVal('TOUCHINGOBJECTMENU', block, blocks))
        return output

    def sensing_touchingcolor(self, block, blocks):
        output = ['touchingColor:']
        output.append(self.converter.inputVal('COLOR', block, blocks))
        return output

    def sensing_coloristouchingcolor(self, block, blocks):
        output = ['color:sees:']
        output.append(self.converter.inputVal('COLOR', block, blocks))
        output.append(self.converter.inputVal('COLOR2', block, blocks))
        return output

    def sensing_distanceto(self, block, blocks):
        output = ['distanceTo:']
        output.append(self.converter.inputVal('DISTANCETOMENU', block, blocks))
        return output

    def sensing_askandwait(self, block, blocks):
        output = ['doAsk']
        output.append(self.converter.inputVal('QUESTION', block, blocks))
        return output

    def sensing_answer(self, block, blocks):
        return ['answer']

    def sensing_keypressed(self, block, blocks):
        output = ['keyPressed:']
        output.append(self.converter.inputVal('KEY_OPTION', block, blocks))
        return output

    def sensing_mousedown(self, block, blocks):
        return ['mousePressed']

    def sensing_mousex(self, block, blocks):
        return ['mouseX']

    def sensing_mousey(self, block, blocks):
        return ['mouseY']

    def sensing_loudness(self, block, blocks):
        return ['soundLevel']

    def sensing_loud(self, block, blocks):
        return ['isLoud']

    def sensing_timer(self, block, blocks):
        return ['timer']

    def sensing_resettimer(self, block, blocks):
        return ['timerReset']

    def sensing_of(self, block, blocks):
        output = ['getAttribute:of:']
        output.append(self.converter.fieldVal('PROPERTY', block))
        output.append(self.converter.inputVal('OBJECT', block, blocks))
        return output

    def sensing_current(self, block, blocks):
        output = ['timeAndDate']
        field = self.converter.fieldVal('CURRENTMENU', block)
        if type(field) == str:
            field = str.lower(field)
        output.append(field)
        return output

    def sensing_dayssince2000(self, block, blocks):
        return ['timestamp']

    def sensing_username(self, block, blocks):
        return ['getUserName']

    def sensing_userid(self, block, blocks):
        return ['getUserId']

    # Operators

    def operator_add(self, block, blocks):
        output = ['+']
        output.append(self.converter.inputVal('NUM1', block, blocks))
        output.append(self.converter.inputVal('NUM2', block, blocks))
        return output

    def operator_subtract(self, block, blocks):
        output = ['-']
        output.append(self.converter.inputVal('NUM1', block, blocks))
        output.append(self.converter.inputVal('NUM2', block, blocks))
        return output

    def operator_multiply(self, block, blocks):
        output = ['*']
        output.append(self.converter.inputVal('NUM1', block, blocks))
        output.append(self.converter.inputVal('NUM2', block, blocks))
        return output

    def operator_divide(self, block, blocks):
        output = ['/']
        output.append(self.converter.inputVal('NUM1', block, blocks))
        output.append(self.converter.inputVal('NUM2', block, blocks))
        return output

    def operator_random(self, block, blocks):
        output = ['randomFrom:to:']
        output.append(self.converter.inputVal('FROM', block, blocks))
        output.append(self.converter.inputVal('TO', block, blocks))
        return output

    def operator_gt(self, block, blocks):
        output = ['>']
        output.append(self.converter.inputVal('OPERAND1', block, blocks))
        output.append(self.converter.inputVal('OPERAND2', block, blocks))
        return output
    
    def operator_lt(self, block, blocks):
        output = ['<']
        output.append(self.converter.inputVal('OPERAND1', block, blocks))
        output.append(self.converter.inputVal('OPERAND2', block, blocks))
        return output
    
    def operator_equals(self, block, blocks):
        output = ['=']
        output.append(self.converter.inputVal('OPERAND1', block, blocks))
        output.append(self.converter.inputVal('OPERAND2', block, blocks))
        return output

    def operator_and(self, block, blocks):
        output = ['&']
        output.append(self.converter.inputVal('OPERAND1', block, blocks))
        output.append(self.converter.inputVal('OPERAND2', block, blocks))
        return output

    def operator_or(self, block, blocks):
        output = ['|']
        output.append(self.converter.inputVal('OPERAND1', block, blocks))
        output.append(self.converter.inputVal('OPERAND2', block, blocks))
        return output

    def operator_not(self, block, blocks):
        output = ['not']
        output.append(self.converter.inputVal('OPERAND', block, blocks))
        return output

    def operator_join(self, block, blocks):
        output = ['concatenate:with:']
        output.append(self.converter.inputVal('STRING1', block, blocks))
        output.append(self.converter.inputVal('STRING2', block, blocks))
        return output

    def operator_letter_of(self, block, blocks):
        output = ['letter:of:']
        output.append(self.converter.inputVal('LETTER', block, blocks))
        output.append(self.converter.inputVal('STRING', block, blocks))
        return output

    def operator_length(self, block, blocks):
        output = ['stringLength:']
        output.append(self.converter.inputVal('STRING', block, blocks))
        return output

    def operator_mod(self, block, blocks):
        output = ['%']
        output.append(self.converter.inputVal('NUM1', block, blocks))
        output.append(self.converter.inputVal('NUM2', block, blocks))
        return output

    def operator_round(self, block, blocks):
        output = ['rounded']
        output.append(self.converter.inputVal('NUM', block, blocks))
        return output
    
    def operator_mathop(self, block, blocks):
        output = ['computeFunction:of:']
        output.append(self.converter.fieldVal('OPERATOR', block))
        output.append(self.converter.inputVal('NUM', block, blocks))
        return output

    # Data

    def data_variable(self, block, blocks):
        output = ['readVariable']
        output.append(self.converter.fieldVal('VARIABLE', block))
        return output   

    def data_setvariableto(self, block, blocks):
        output = ['setVar:to:']
        output.append(self.converter.fieldVal('VARIABLE', block))
        output.append(self.converter.inputVal('VALUE', block, blocks))
        return output

    def data_changevariableby(self, block, blocks):
        output = ['changeVar:by:']
        output.append(self.converter.fieldVal('VARIABLE', block))
        output.append(self.converter.inputVal('VALUE', block, blocks))
        return output

    def data_showvariable(self, block, blocks):
        output = ['showVariable:']
        output.append(self.converter.fieldVal('VARIABLE', block))
        return output

    def data_hidevariable(self, block, blocks):
        output = ['hideVariable:']
        output.append(self.converter.fieldVal('VARIABLE', block))
        return output

    def data_listcontents(self, block, blocks):
        output = ['contentsOfList:']
        output.append(self.converter.fieldVal('LIST', block))
        return output
    
    def data_addtolist(self, block, blocks):
        output = ['append:toList:']
        output.append(self.converter.inputVal('ITEM', block, blocks))
        output.append(self.converter.fieldVal('LIST', block))
        return output

    def data_deleteoflist(self, block, blocks):
        output = ['deleteLine:ofList:']
        output.append(self.converter.inputVal('INDEX', block, blocks))
        output.append(self.converter.fieldVal('LIST', block))
        return output
    
    def data_deletealloflist(self, block, blocks):
        output = ['deleteLine:ofList:', 'all']
        output.append(self.converter.fieldVal('LIST', block))
        return output

    def data_insertatlist(self, block, blocks):
        output = ['insert:at:ofList:']
        output.append(self.converter.inputVal('ITEM', block, blocks))
        output.append(self.converter.inputVal('INDEX', block, blocks))
        output.append(self.converter.fieldVal('LIST', block))
        return output

    def data_replaceitemoflist(self, block, blocks):
        output = ['setLine:ofList:to:']
        output.append(self.converter.inputVal('INDEX', block, blocks))
        output.append(self.converter.fieldVal('LIST', block))
        output.append(self.converter.inputVal('ITEM', block, blocks))
        return output

    def data_itemoflist(self, block, blocks):
        output = ['getLine:ofList:']
        output.append(self.converter.inputVal('INDEX', block, blocks))
        output.append(self.converter.fieldVal('LIST', block))
        return output

    def data_lengthoflist(self, block, blocks):
        output = ['lineCountOfList:']
        output.append(self.converter.fieldVal('LIST', block))
        return output

    def data_listcontainsitem(self, block, blocks):
        output = ['list:contains:']
        output.append(self.converter.fieldVal('LIST', block))
        output.append(self.converter.inputVal('ITEM', block, blocks))
        return output

    def data_showlist(self, block, blocks):
        output = ['showList:']
        output.append(self.converter.fieldVal('LIST', block))
        return output

    def data_hidelist(self, block, blocks):
        output = ['hideList:']
        output.append(self.converter.fieldVal('LIST', block))
        return output

    # Procedures

    def procedures_definition(self, block, blocks):
        block = blocks[block['inputs']['custom_block'][1]]
        procData = block['mutation']
        output = ['procDef']
        output.append(procData['proccode'])
        output.append(json.loads(procData['argumentnames']))
        output.append(json.loads(procData['argumentdefaults']))
        self.converter.blockID += (1 + len(output[-2]))
        if len(output[-1]) != len(output[-2]):
            output[-1] = len(output[-2]) * ['']
        warp = procData['warp']
        output.append(warp == 'true' or (type(warp) == bool and warp))
        return output

    def procedures_call(self, block, blocks):
        output = ['call']
        output.append(block['mutation']['proccode'])
        ids = json.loads(block['mutation']['argumentids'])
        for i in ids:
            output.append(self.converter.inputVal(i, block, blocks))
        return output

    def argument_reporter_string_number(self, block, blocks):
        output = ['getParam']
        output.append(self.converter.fieldVal('VALUE', block))
        output.append('r')
        return output

    def argument_reporter_boolean(self, block, blocks):
        output = ['getParam']
        output.append(self.converter.fieldVal('VALUE', block))
        output.append('b')
        return output

    # LEGO WeDo 2.0

    def wedo2_motorOnFor(self, block, blocks):
        output = ['LEGO WeDo 2.0\u001fmotorOnFor']
        output.append(self.converter.inputVal('MOTOR_ID', block, blocks))
        output.append(self.converter.inputVal('DURATION', block, blocks))
        return output

    def wedo2_motorOn(self, block, blocks):
        output = ['LEGO WeDo 2.0\u001fmotorOn']
        output.append(self.converter.inputVal('MOTOR_ID', block, blocks))
        return output

    def wedo2_motorOff(self, block, blocks):
        output = ['LEGO WeDo 2.0\u001fmotorOff']
        output.append(self.converter.inputVal('MOTOR_ID', block, blocks))
        return output
    
    def wedo2_startMotorPower(self, block, blocks):
        output = ['LEGO WeDo 2.0\u001fstartMotorPower']
        output.append(self.converter.inputVal('MOTOR_ID', block, blocks))
        output.append(self.converter.inputVal('POWER', block, blocks))
        return output

    def wedo2_setMotorDirection(self, block, blocks):
        output = ['LEGO WeDo 2.0\u001fsetMotorDirection']
        output.append(self.converter.inputVal('MOTOR_ID', block, blocks))
        output.append(self.converter.inputVal('MOTOR_DIRECTION', block, blocks))
        return output

    def wedo2_setLightHue(self, block, blocks):
        output = ['LEGO WeDo 2.0\u001fsetLED']
        output.append(self.converter.inputVal('HUE', block, blocks))
        return output

    def wedo2_playNoteFor(self, block, blocks):
        output = ['LEGO WeDo 2.0\u001fplayNote']
        output.append(self.converter.inputVal('NOTE', block, blocks))
        output.append(self.converter.inputVal('DURATION', block, blocks))
        return output

    def wedo2_whenDistance(self, block, blocks):
        output = ['LEGO WeDo 2.0\u001fwhenDistance']
        output.append(self.converter.inputVal('OP', block, blocks))
        output.append(self.converter.inputVal('REFERENCE', block, blocks))
        return output

    def wedo2_whenTilted(self, block, blocks):
        output = ['LEGO WeDo 2.0\u001fwhenTilted']
        output.append(self.converter.inputVal('TILT_DIRECTION_ANY', block, blocks))
        return output

    def wedo2_getDistance(self, block, blocks):
        return ['LEGO WeDo 2.0\u001fgetDistance']

    def wedo2_isTilted(self, block, blocks):
        output = ['LEGO WeDo 2.0\u001fisTilted']
        output.append(self.converter.inputVal('TILT_DIRECTION_ANY', block, blocks))
        return output

    def wedo2_getTiltAngle(self, block, blocks):
        output = ['LEGO WeDo 2.0\u001fgetTilt']
        output.append(self.converter.inputVal('TILT_DIRECTION', block, blocks))
        return output

class ProjectConverter:

    varModes = {
        'default': 1,
        'large': 2,
        'slider': 3
    }

    rotationStyles = {
        'all around': 'normal',
        'left-right': 'leftRight',
        'don\'t rotate': 'none'
    }

    @staticmethod
    def hexToDec(hexNum):
        try:
            return int(hexNum[1:], 16)
        except:
            return hexNum

    @staticmethod
    def specialNum(num):
        if num == '-Infinity':
            return float('-inf')
        if num == 'Infinity':
            return float('inf')
        if num == 'NaN':
            return float('nan')
        return num

    def __init__(self):
        self.argmapper = BlockArgMapper(self)
        self.blockID = 0
        self.comments = []
        self.blockComments = {}

    def generateWarning(self, message):
        self.warnings += 1
        printWarning(message)

    def setCommentBlockId(self, id):
        if id in self.blockComments:
            self.comments[self.blockComments[id]][5] = self.blockID
    
    def hackedReporterBlockID(self, reporter):
        self.blockID += 1
        for value in reporter:
            if type(value) == list:
                self.hackedReporterBlockID(value)

    def convertBlock(self, block, blocks):
        opcode = block['opcode']
        self.blockID += 1
        try:
            return self.argmapper.mapArgs(opcode, block, blocks)
        except:
            if len(block['inputs']) == 0 and len(block['fields']) == 1 and block['shadow']: # Menu opcodes and shadows
                self.blockID -= 1
                return self.fieldVal(list(block['fields'].items())[0][0], block)
            else:
                self.generateWarning("Incompatible opcode '{}'".format(opcode))
                
                output = [opcode]
                for i in block['inputs']:
                    output.append(self.inputVal(i, block, blocks))
                for f in block['fields']:
                    output.append(self.fieldVal(f, block))
                return output

    def inputVal(self, value, block, blocks):

        if not value in block['inputs']:
            return False

        value = block['inputs'][value]
        if value[1] == None:
            return None
        if value[0] == 1:
            if type(value[1]) == str:
                self.setCommentBlockId(value[1])
                return self.convertBlock(blocks[value[1]], blocks)
            else:
                output = value[1][1]        
        else:
            out = value[1]
            if type(out) == str:
                self.setCommentBlockId(out)
                return self.convertBlock(blocks[out], blocks)
            else:
                if out[0] == 12:
                    self.blockID += 1
                    return ['readVariable', out[1]]
                elif out[0] == 13:
                    self.blockID += 1
                    return ['contentsOfList:', out[1]]
                else:
                    try:
                        return out[1]
                    except:
                        return
        
        outType = value[1][0]
        if outType in [4, 5, 8]:
            try:
                string = str(output)
                output = float(output)
                if output % 1 == 0 and not ('.' in string):
                    output = int(output)
            except ValueError:
                pass
        elif outType in [6, 7]:
            try:
                output = float(output)
                if output % 1 == 0:
                    output = int(output)
            except ValueError:
                pass
        elif outType == 9:
            output = ProjectConverter.hexToDec(output)

        return ProjectConverter.specialNum(output)

    def fieldVal(self, value, block):

        if not value in block['fields']:
            return None

        value = block['fields'][value][0]
        if type(value) == list:
            self.hackedReporterBlockID(value)

        return value

    def convertSubstack(self, key, blocks):
        self.setCommentBlockId(key)
        block = blocks[key]
        script = []
        end = False
        while not end:
            script.append(self.convertBlock(block, blocks))
            if block['next'] == None:
                end = True
            else:
                self.setCommentBlockId(block['next'])
                block = blocks[block['next']]
        return script

    def substackVal(self, stack, block, blocks):

        if not stack in block['inputs']:
            return None

        stack = block['inputs'][stack]
        if len(stack) < 2 or stack[1] == None:
            return []

        return self.convertSubstack(stack[1], blocks)

    def addComment(self, c):
        comment = []
        if c['x'] == None:
            x = None
        else:
            x = round(c['x'] / 1.5, 6)
            if x % 1 == 0:
                x = int(x)
        comment.append(x)
        if c['y'] == None:
            y = None
        else:
            y = round(c['y'] / 1.8, 6)
            if y % 1 == 0:
                y = int(y)
        comment.append(y)
        comment.append(c['width'])
        comment.append(c['height'])
        comment.append(not c['minimized'])
        comment.append(-1)
        comment.append(c['text'])

        if c['blockId'] != None:
            self.blockComments[c['blockId']] = len(self.comments)
        
        self.comments.append(comment)

    def addSound(self, s):

        if not s['assetId'] in self.soundAssets:
            self.soundAssets[s['assetId']] = len(self.soundAssets)
            if s['dataFormat'] == 'wav':
                f = self.zfsb3.open(s['md5ext'], 'r')
                self.zfsb2.writestr('{}.{}'.format(len(self.soundAssets) - 1, s['dataFormat']), bytes(f.read()))
                f.close()
            else:
                self.generateWarning("Audio file '{}' cannot be converted into WAV".format(s['md5ext']))
        
        sound = {
            'soundName': s['name'],
            'soundID': self.soundAssets[s['assetId']],
            'md5': s['assetId'] + '.wav',
            'sampleCount': s['sampleCount'],
            'rate': s['rate'],
            'format': 'adpcm'
        }

        self.sounds.append(sound)

    def addCostume(self, c):
        
        if not c['assetId'] in self.costumeAssets:
            self.costumeAssets[c['assetId']] = len(self.costumeAssets)

            f = self.zfsb3.open(c['md5ext'], 'r')
            img = f.read()
            if c['dataFormat'] == 'svg':
                img = str(img)[2:-1]
                img = img.replace('\\n', '\n')
                img = img.replace("\\'", "&apos;")
                img = img.replace('\\\\', '\\')
                img = img.replace('fill="undefined"', '') # Fix broken SVGs
                img = img.replace('font-family="Sans Serif"', 'font-family="Helvetica"')
                img = img.replace('font-family="Serif"', 'font-family="Donegal"')
                img = img.replace('font-family="Handwriting"', 'font-family="Gloria"')
                img = img.replace('font-family="Curly"', 'font-family="Mystery"')
            else:
                img = bytes(img)
            self.zfsb2.writestr('{}.{}'.format(len(self.costumeAssets) - 1, c['dataFormat']), img)
            f.close()

        costume = {
            'costumeName': c['name'],
            'baseLayerID': self.costumeAssets[c['assetId']],
            'baseLayerMD5': c['md5ext'],
            'rotationCenterX': c['rotationCenterX'],
            'rotationCenterY': c['rotationCenterY']
        }

        if 'bitmapResolution' in c:
            costume['bitmapResolution'] = c['bitmapResolution']

        self.costumes.append(costume)

    def convertTarget(self, target, index):

        sprite = {}
        
        sprite['objName'] = target['name']
        scripts = []
        variables = []
        lists = []
        self.sounds = []
        self.costumes = []
        self.comments = []

        isStage = target['isStage']

        for s in target['sounds']:
            self.addSound(s)

        for c in target['costumes']:
            self.addCostume(c)

        for key, v in target['variables'].items():
            variable = {
                'name': v[0],
                'value': ProjectConverter.specialNum(v[1]),
                'isPersistent': len(v) >= 3 and v[2]
            }
            variables.append(variable)

        for key, l in target['lists'].items():
            ls = {
                'listName': l[0],
                'contents': [ProjectConverter.specialNum(item) for item in l[1]],
                'isPersistent': False
            }
            lists.append(ls)

        self.blockComments = {}

        for key, c in target['comments'].items():
            self.addComment(c)
        
        blocks = target['blocks'] 
        self.blockID = 0

        for key, b in blocks.items():

            if type(b) == list:

                x = round(b[3] / 1.5, 6)
                if x % 1 == 0:
                    x = int(x)
                y = round(b[4] / 1.8, 6)
                if y % 1 == 0:
                    y = int(y)
                script = [x, y]

                if b[0] == 12:
                    script.append([['readVariable', b[1]]])
                elif b[0] == 13:
                    script.append([['contentsOfList:', b[1]]])
                else:
                    script = None

                if script != None:
                    self.setCommentBlockId(key)
                    self.blockID += 1
                    scripts.append(script)
                    self.scriptCount += 1

            elif b['topLevel']:

                x = round(b['x'] / 1.5, 6)
                if x % 1 == 0:
                    x = int(x)
                y = round(b['y'] / 1.8, 6)
                if y % 1 == 0:
                    y = int(y)
                
                scripts.append([x, y, self.convertSubstack(key, blocks)])
                self.scriptCount += 1
        
        sprite['scripts'] = scripts
        sprite['variables'] = variables
        sprite['lists'] = lists
        sprite['sounds'] = self.sounds
        sprite['costumes'] = self.costumes
        sprite['scriptComments'] = self.comments

        if isStage:

            sprite['currentCostumeIndex'] = target['currentCostume']
            sprite['tempoBPM'] = target['tempo']
            sprite['videoAlpha'] = (100 - target['videoTransparency']) / 100

            sprite['objName'] = 'Stage'
            sprite['info'] = {
                'userAgent': self.jsonData['meta']['agent'],
                'videoOn': target['videoState'] == 'on'
            }

        else:

            sprite['currentCostumeIndex'] = target['currentCostume']
            sprite['scratchX'] = target['x']
            sprite['scratchY'] = target['y']
            sprite['scale'] = target['size'] / 100
            sprite['direction'] = target['direction']
            sprite['rotationStyle'] = ProjectConverter.rotationStyles[target['rotationStyle']]
            sprite['isDraggable'] = target['draggable']
            sprite['indexInLibrary'] = index
            sprite['visible'] = target['visible']
            sprite['spriteInfo'] = {}

        print("Finished converting '{}' ({}/{})".format(sprite['objName'], index + 1, self.totalTargets))

        return (isStage, sprite) 

    def updateList(self, l, ls):
        l['x'] = ls['x']
        l['y'] = ls['y']
        l['width'] = ls['width']
        l['height'] = ls['height']
        l['visible'] = ls['visible']

    # Update list data with monitor info

    def updateListData(self, output, sprites, lists):

        for l in output['lists']:

            if l['listName'] in lists['Stage']:
                ls = lists['Stage'][l['listName']]
                self.updateList(l, ls)

        for s in sprites:
            spriteName = s['objName']

            if spriteName in lists:
                for l in s['lists']:

                    if l['listName'] in lists[spriteName]:
                        ls = lists[spriteName][l['listName']]
                        self.updateList(l, ls)

    def addMonitor(self, m):

        if m['opcode'] == 'data_variable':
            
            sMin = m['min'] if 'min' in m else m['sliderMin']
            sMax = m['max'] if 'max' in m else m['sliderMax']
            monitor = {
                'target': 'Stage' if m['spriteName'] == None else m['spriteName'],
                'cmd': 'getVar:',
                'param': m['params']['VARIABLE'],
                'color': 15629590,
                'label': ("" if m['spriteName'] == None else (m['spriteName'] + ": ")) + m['params']['VARIABLE'],
                'mode': ProjectConverter.varModes[m['mode']],
                'sliderMin': sMin,
                'sliderMax': sMax,
                'isDiscrete': sMin % 1 == 0 and sMax % 1 == 0 and not('.' in str(sMin)) and not('.' in str(sMax)),
                'x': m['x'],
                'y': m['y'],
                'visible': m['visible']
            }
            self.monitors.append(monitor)

        elif m['opcode'] == 'data_listcontents':

            monitor = {
                'listName': m['params']['LIST'],
                'contents': m['value'],
                'isPersistent': False,
                'x': m['x'],
                'y': m['y'],
                'width': m['width'],
                'height': m['height'],
                'visible': m['visible']
            }

            self.monitors.append(monitor)

            spriteName = 'Stage' if m['spriteName'] == None else m['spriteName']
            if not spriteName in self.lists:
                self.lists[spriteName] = {}

            self.lists[spriteName][monitor['listName']] = {
                'x': m['x'],
                'y': m['y'],
                'width': m['width'],
                'height': m['height'],
                'visible': m['visible']
            }

        else:
            # Non-variable and non-list monitor (ex: x-position, y-position, volume, etc.)
            self.generateWarning("Stage monitor '{}' will not be converted".format(m['opcode']))

    def convertProject(self, sb3path, sb2path, replace = False):
        
        try:
            self.zfsb3 = zipfile.ZipFile(sb3path, 'r')
        except:
            printError("File '{}' does not exist".format(sb3path))

        try:
            self.zfsb2 = zipfile.ZipFile(sb2path, 'x')
        except:
            if replace:
                import os
                os.remove(sb2path)
                self.zfsb2 = zipfile.ZipFile(sb2path, 'x')
            else:
                printError("File '{}' already exists".format(sb2path))

        f = self.zfsb3.open('project.json', 'r')
        self.jsonData = json.loads(f.read())
        f.close()

        output = {}
        self.costumeAssets = {}
        self.soundAssets = {}

        sprites = []

        targetsDone = 0
        
        self.totalTargets = len(self.jsonData['targets'])
        self.scriptCount = 0
        self.warnings = 0

        # Convert Stage and sprites

        for target in self.jsonData['targets']:
            sprite = self.convertTarget(target, targetsDone)
            if sprite[0]:
                output = sprite[1]
            else:
                sprites.append(sprite[1])
            targetsDone += 1

        output['info']['scriptCount'] = self.scriptCount
        output['info']['spriteCount'] = self.totalTargets - 1

        self.monitors = []

        self.lists = {}

        # Convert monitors

        for m in self.jsonData['monitors']:
            self.addMonitor(m)

        self.updateListData(output, sprites, self.lists)

        sprites.extend(self.monitors)

        output['children'] = sprites

        # Add WeDo 2.0 extension if necessary

        if 'wedo2' in self.jsonData['extensions']:
            output['info']['savedExtensions'] = [{'extensionName': 'LEGO WeDo 2.0'}]

        output = json.dumps(output)

        self.zfsb2.writestr('project.json', output)

        return self.warnings

if __name__ == '__main__':

    dialog = False
    if len(sys.argv) < 3:
        dialog = True
        import tkinter
        from tkinter import filedialog
        root = tkinter.Tk()
        root.withdraw()
        sb3path = filedialog.askopenfilename(title = "Open SB3 Project", filetypes = [("Scratch 3 Project", "*.sb3")])
        sb2path = filedialog.asksaveasfilename(title = "Save as SB2 Project", filetypes = [("Scratch 2 Project", "*.sb2")])
    else:
        sb3path = sys.argv[1]
        sb2path = sys.argv[2]
    
    if not sb3path[-3:] == 'sb3' or not sb2path[-3:] == 'sb2':
        printError("Incorrect file extensions")
    
    warnings = ProjectConverter().convertProject(sb3path, sb2path, replace = dialog)

    if warnings == 0:
        print('Completed with no warnings')
    elif warnings == 1:
        print('Completed with {} warning'.format(warnings))
    else:
        print('Completed with {} warnings'.format(warnings))