import sys, json, zipfile, audioop, hashlib

sys.setrecursionlimit(4100)

def printWarning(message):
    print("WARNING: " + message)

def printError(message):
    lines = message.split('\n')
    lines = ["       " + line for line in lines]
    lines[0] = "ERROR: " + lines[0][7:]
    print('\n'.join(lines))
    input('Press enter to exit... ')
    exit()

class BlockArgMapper:
    
    stageAttrs = {
        'backdrop #',
        'backdrop name',
        'volume'
    }

    spriteAttrs = {
        'x position',
        'y position',
        'direction',
        'costume #',
        'costume name',
        'size',
        'volume'
    }

    def __init__(self, obj):
        assert type(obj) == ProjectConverter
        self.converter = obj

    def mapArgs(self, opcode, block, blocks):
        assert not opcode.startswith('__')
        return getattr(self, opcode)(block, blocks)

    def varName(self, name):
        if type(name) == str:
            return ('_' if self.converter.compat else '') + name
        else:
            if self.converter.compat:
                return ['concatenate:with:', '_', name]
            else:
                return name

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
            return ['goBackByLayers:', 1.79e+308]

    def looks_goforwardbackwardlayers(self, block, blocks):
        layers = self.converter.inputVal('NUM', block, blocks)
        field = self.converter.fieldVal('FORWARD_BACKWARD', block)
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
            if not self.converter.convertingMonitors:
                if self.converter.compat: # Can't use getAttribute:of: because it doesn't work for clones
                    self.converter.costumeName = True
                    return ['getLine:ofList:', ['costumeIndex'], self.converter.compatVarName('costume names')]
                else:
                    self.converter.generateWarning("Incompatible block 'costume [name v]'")
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
        if self.converter.compat:
            self.converter.penUpDown = True
            return ['call', 'pen down']
        else:
            return ['putPenDown']

    def pen_penUp(self, block, blocks):
        if self.converter.compat:
            self.converter.penUpDown = True
            return ['call', 'pen up']
        else:
            return ['putPenup']

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
            if type(value) == str:
                try:
                    value = float(value)
                except:
                    pass
            if type(value) == float or type(value) == int:
                value *= 2
            else:
                value = ['*', 2, value]
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
            if type(value) == str:
                try:
                    value = float(value)
                except:
                    pass
            if type(value) == float or type(value) == int:
                value *= 2
            else:
                value = ['*', 2, value]
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

    def sensing_setdragmode(self, block, blocks):
        assert self.converter.compat
        self.converter.dragMode = True
        return ['call', 'set drag mode %s', self.converter.fieldVal('DRAG_MODE', block)]

    def sensing_loudness(self, block, blocks):
        return ['soundLevel']

    def sensing_loud(self, block, blocks):
        return ['isLoud']

    def sensing_timer(self, block, blocks):
        return ['timer']

    def sensing_resettimer(self, block, blocks):
        return ['timerReset']

    def sensing_of(self, block, blocks):
        attr = self.converter.fieldVal('PROPERTY', block)
        obj = self.converter.inputVal('OBJECT', block, blocks)
        if obj == '_stage_':
            if (type(attr) == list) or (attr not in BlockArgMapper.stageAttrs):
                attr = self.varName(attr)
        elif (type(attr) == list) or (attr not in BlockArgMapper.spriteAttrs):
            attr = self.varName(attr)
        return ['getAttribute:of:', attr, obj]

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
        if not self.converter.convertingMonitors:
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
        output.append(self.varName(procData['proccode']))
        output.append(json.loads(procData['argumentnames']))
        output.append(json.loads(procData['argumentdefaults']))
        if len(output[-1]) != len(output[-2]):
            output[-1] = len(output[-2]) * ['']
        warp = procData['warp']
        output.append(warp == 'true' or (type(warp) == bool and warp))
        return output

    def procedures_call(self, block, blocks):
        output = ['call']
        output.append(self.varName(block['mutation']['proccode']))
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

    monitorColors = {
        'motion': 4877524,
        'looks': 9065943,
        'sound': 12272323,
        'music': 12272323,
        'sensing': 2926050,
        'data': 15629590
    }

    # Used to change variable names in hacked reporters if in compatibility mode
    sb2BlocksVarFields = {
        'setVar:to:': 1,
        'changeVar:by:': 1,
        'showVariable:': 1,
        'hideVariable:': 1,
        'readVariable': 1,
        'contentsOfList:': 1,
        'append:toList:': 2,
        'deleteLine:ofList:': 2,
        'insert:at:ofList:': 3,
        'setLine:ofList:to:': 2,
        'getLine:ofList:': 2,
        'lineCountOfList:': 1,
        'list:contains:': 1,
        'showList:': 1,
        'hideList:': 1
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
        self.convertingMonitors = False

    def varName(self, name):
        if type(name) == str:
            return ('_' if self.compat else '') + name
        else:
            if self.compat:
                return ['concatenate:with:', '_', name]
            else:
                return name

    def compatVarName(self, name):
        return ('Stage: ' if self.targetIsStage else '') + name

    def generateWarning(self, message):
        self.warnings += 1
        printWarning(message)

    def setCommentBlockID(self, id):
        if id in self.blockComments:
            self.comments[self.blockComments[id]][5] = self.blockID

    def convertHackedReporter(self, reporter):
        if self.compat: # Add underscore to variable names if in compatibility mode
            block = reporter[0]
            if block in ProjectConverter.sb2BlocksVarFields:
                index = ProjectConverter.sb2BlocksVarFields[block]
                reporter[index] = self.varName(reporter[index])
            elif block == 'getAttribute:of:':
                if reporter[2] == '_stage_':
                    if reporter[1] not in BlockArgMapper.stageAttrs:
                        reporter[1] = self.varName(reporter[1])
                elif reporter[1] not in BlockArgMapper.spriteAttrs:
                    reporter[1] = self.varName(reporter[1])
            for value in reporter:
                if type(value) == list:
                    self.convertHackedReporter(value)

    def convertBlock(self, block, blocks):
        opcode = block['opcode']
        try:
            output = self.argmapper.mapArgs(opcode, block, blocks)
            output.append(tuple([block['UID']]))
            return output
        except:
            if len(block['inputs']) == 0 and len(block['fields']) == 1 and block['shadow'] and not block['topLevel']:  # Menu opcodes and shadows
                return self.fieldVal(list(block['fields'].items())[0][0], block)
            else:
                self.generateWarning("Incompatible opcode '{}'".format(opcode))

                output = [opcode]
                for i in block['inputs']:
                    value = self.inputVal(i, block, blocks)
                    if type(value) != list:
                        output.append(value)
                for f in block['fields']:
                    value = self.fieldVal(f, block)
                    if type(value) != list:
                        output.append(value)
                output.append(tuple([block['UID']]))
                return output

    def inputVal(self, value, block, blocks):

        if not value in block['inputs']:
            return False

        value = block['inputs'][value]
        if value[1] == None:
            return None
        if value[0] == 1:
            if type(value[1]) == str:
                return self.convertBlock(blocks[value[1]], blocks)
            else:
                output = value[1][1]
        else:
            out = value[1]
            if type(out) == list:
                if out[0] == 12:
                    return ['readVariable', self.varName(out[1])]
                elif out[0] == 13:
                    return ['contentsOfList:', self.varName(out[1])]
                else:
                    try:
                        return out[1]
                    except:
                        return
            else:
                try:
                    return self.convertBlock(blocks[out], blocks)
                except:
                    return False

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

        output = block['fields'][value][0]
        if type(output) == list:
            self.convertHackedReporter(output)
        if value in ['VARIABLE', 'LIST']:
            output = self.varName(output)

        return output

    def convertSubstack(self, key, blocks):
        block = blocks[key]
        script = []
        end = False
        while not end:
            script.append(self.convertBlock(block, blocks))
            if block['next'] == None:
                end = True
            else:
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

        scount = s['sampleCount']
        srate = s['rate']

        if not s['assetId'] in self.soundAssets:

            md5 = s['assetId']
            self.soundAssets[s['assetId']] = [len(self.soundAssets)]

            if s['dataFormat'] == 'wav':
                f = self.zfsb3.open(s['md5ext'], 'r')
                wav = bytes(f.read())

                width = int.from_bytes(wav[34:36], byteorder='little') // 8
                channels = int.from_bytes(wav[22:24], byteorder='little')
                srate = int.from_bytes(wav[24:28], byteorder='little')

                modified = False
                error = width * channels == 0 or (len(wav) - 44) % (width * channels) != 0
                
                if not error:
                    if channels == 2: # Convert to mono
                        wav = wav[0:44] + audioop.tomono(wav[44:], width, 1, 1)
                        modified = True
                    
                    if srate > 22050 and not error: # Downsample
                        wav = wav[0:44] + audioop.ratecv(wav[44:], width, 1, srate, 22050, None)[0]
                        srate = 22050
                        modified = True

                if modified:
                    size = len(wav) - 44
                    wav = wav[0:22] + (1).to_bytes(2, byteorder='little') + srate.to_bytes(4, byteorder='little') + wav[28:40] + size.to_bytes(4, byteorder='little') + wav[44:]
                    scount = size // width
                    self.soundAssets[s['assetId']].append(False)
                    md5 = hashlib.md5(wav).hexdigest()
                elif error and not srate <= 22050 and not channels == 1:
                    srate = s['rate']
                    self.soundAssets[s['assetId']].append(True)
                else:
                    self.soundAssets[s['assetId']].append(False)

                self.zfsb2.writestr('{}.{}'.format(len(self.soundAssets) - 1, s['dataFormat']), wav)
                f.close()
            else:
                self.soundAssets[s['assetId']].append(False)
            
            self.soundAssets[s['assetId']].append(scount)
            self.soundAssets[s['assetId']].append(srate)
            self.soundAssets[s['assetId']].append(md5)

        if s['dataFormat'] != 'wav':
            self.generateWarning("Sound '{}' cannot be converted into WAV".format(s['name']))
        elif self.soundAssets[s['assetId']][1] == True:
            self.generateWarning("Sound '{}' cannot be converted to mono or downsampled".format(s['name']))

        fileData = self.soundAssets[s['assetId']]
        sound = {
            'soundName': s['name'],
            'soundID': fileData[0],
            'md5': fileData[4] + '.wav',
            'sampleCount': fileData[2],
            'rate': fileData[3],
            'format': ''
        }

        self.sounds.append(sound)

    def addCostume(self, c):

        if not c['assetId'] in self.costumeAssets:
            md5ext = c['md5ext']
            self.costumeAssets[c['assetId']] = [len(self.costumeAssets)]

            f = self.zfsb3.open(c['md5ext'], 'r')
            img = f.read()
            if c['dataFormat'] == 'svg':
                img = str(img, encoding='utf-8')

                # Remove incorrect attributes added by Scratch 3.0
                # The correct values are found in the style attribute

                img = img.replace('fill="undefined"', '')  # Remove undefined fill
                
                # Remove incorrect stroke-width
                if ';stroke-width:' in img: # Check if stroke-width is in style attribute (may incorrectly remove some stroke-width attributes)
                    left = 0 
                    while left != -1:
                        left = img.find('stroke-width="', left)
                        if left != -1:
                            right = img.find('"', left + 14) + 1
                            img = img[0:left] + '' + img[right:]
                            left = right

                # Reposition bitmap images to their correct position

                if 'image' in img:

                    left = 0
                    while left != -1:
                        left = img.find('<image ', left)
                        if left != -1:
                            right = img.find('xlink:href=', left)
                            image = img[left:right]

                            try:
                                xLeft = image.find('x="')
                                xRight = image.find('"', xLeft + 3)
                                trX = float(image[xLeft+3:xRight])
                                image = image[0:xLeft] + image[xRight+1:]

                                yLeft = image.find('y="')
                                yRight = image.find('"', yLeft + 3)
                                trY = float(image[yLeft+3:yRight])
                                image = image[0:yLeft] + image[yRight+1:]

                                transformLeft = image.find('transform="')
                                transformRight = image.find('"', transformLeft + 11)
                                image = image[0:transformRight] + 'translate({} {})'.format(trX, trY) + image[transformRight:]

                                img = img[0:left] + image + img[right:]
                            except:
                                # self.generateWarning("Costume '{}' may have incorrect bitmap image positioning".format(c['name']))
                                pass

                            left += 1

                # Replace tspan elements with text elements, which aren't supported by Scratch 2.0

                if 'tspan' in img:

                    newImg = ''
                    left = 0
                    while left != -1:
                        oldLeft = left
                        left = img.find('<text', left)
                        if left != -1:
                            newImg += img[oldLeft:left]
                            right = img.find('</text>', left) + 7

                            innerLeft = img.find('>', left) + 1
                            attrs = img[left:innerLeft - 1] + ' '
                            i = attrs.find('id="') # Remove id attribute
                            if i != -1:
                                j = attrs.find('"', i + 4)
                                attrs = attrs[0:i] + attrs[j+1:]
                            attrs = attrs.replace('font-family="Sans Serif"', 'font-family="Helvetica"')
                            attrs = attrs.replace('font-family="Serif"', 'font-family="Donegal"')
                            attrs = attrs.replace('font-family="Handwriting"', 'font-family="Gloria"')
                            attrs = attrs.replace('font-family="Curly"', 'font-family="Mystery"')
                            attrs = attrs.replace('xml:space="preserve"', '')

                            left = right

                            # Remove tspan elements
                            text = ''
                            lineCount = 0
                            content = img[innerLeft:right - 7]
                            if 'tspan' in content:
                                while innerLeft != -1:
                                    innerLeft = img.find('<tspan', innerLeft, right)
                                    if innerLeft != -1:
                                        lineCount += 1
                                        innerLeft += 6
                                        innerLeft = img.find('>', innerLeft, right) + 1
                                        innerRight = img.find('</tspan>', innerLeft, right)
                                        text += img[innerLeft:innerRight] + '\n'
                                        innerLeft = innerRight + 7
                                
                                text = text[0:-1]
                                text = text + '</text>'
                            else:
                                text += content + '</text>'

                            # Fix misplaced text
                            matLeft = attrs.find('matrix')
                            if matLeft != -1:
                                try:
                                    matRight = attrs.find('"', matLeft)
                                    matrix = attrs[matLeft:matRight].split(' ')
                                    x = matrix[-2]
                                    if x[-1] == ',':
                                        x = x[0:-1]
                                    scX = matrix[0][7:]
                                    if scX[-1] == ',':
                                        scX = scX[0:-1]
                                    matrix[-2] = str(float(x) - 2.5 * float(scX))
                                    scY = matrix[3]
                                    if scY[-1] == ',':
                                        scY = scY[0:-1]
                                    matrix[-1] = str(float(matrix[-1][0:-1]) + 2.5 * float(scY)) + ')'
                                    matrix = ' '.join(matrix)
                                    attrs = attrs[0:matLeft] + matrix + attrs[matRight:]
                                except:
                                    self.generateWarning("Costume '{}' may have incorrect text positioning".format(c['name']))
                            else:
                                trLeft = attrs.find('translate')
                                scLeft = attrs.find('scale')
                                if not (trLeft == -1 or scLeft == -1):
                                    try:
                                        scRight = attrs.find('"', scLeft)

                                        i = trLeft + 10
                                        trX = ''
                                        while attrs[i] not in ', ':
                                            trX += attrs[i]
                                            i += 1
                                        while attrs[i] in ', ':
                                            i += 1
                                        trY = ''
                                        while attrs[i] not in ' )':
                                            trY += attrs[i]
                                            i += 1
                                        trX = float(trX)
                                        trY = float(trY)

                                        i = scLeft + 6
                                        scX = ''
                                        while attrs[i] not in ', ':
                                            scX += attrs[i]
                                            i += 1
                                        while attrs[i] in ', ':
                                            i += 1
                                        scY = ''
                                        while attrs[i] not in ' )':
                                            scY += attrs[i]
                                            i += 1
                                        scX = float(scX)
                                        scY = float(scY)
                                        if lineCount > 1:
                                            trY -= 40 * scY
                                        else:
                                            trY -= 25 * scY
                                        matrix = 'matrix({} 0 0 {} {} {})'.format(scX, scY, trX, trY)
                                        attrs = attrs[0:trLeft] + matrix + attrs[scRight:]
                                    except:
                                        self.generateWarning("Costume '{}' may have incorrect text positioning".format(c['name']))

                            text = attrs + '>' + text
                            newImg += text
                            left = right
                        else:
                            newImg += img[oldLeft:]

                    img = newImg
                
                md5ext = hashlib.md5(img.encode('utf-8')).hexdigest() + '.svg'
            else:
                img = bytes(img)
            self.zfsb2.writestr('{}.{}'.format(len(self.costumeAssets) - 1, c['dataFormat']), img)
            f.close()

            self.costumeAssets[c['assetId']].append(md5ext)

        fileData = self.costumeAssets[c['assetId']]
        costume = {
            'costumeName': c['name'],
            'baseLayerID': fileData[0],
            'baseLayerMD5': fileData[1],
            'rotationCenterX': c['rotationCenterX'],
            'rotationCenterY': c['rotationCenterY']
        }

        if 'bitmapResolution' in c:
            costume['bitmapResolution'] = c['bitmapResolution']

        self.costumes.append(costume)

    def getCommentBlockIDs(self, script):
        if len(script) > 0:
            UID = script[-1]
            if type(UID) == tuple:
                self.setCommentBlockID(UID[0])
                del script[-1]
            if type(script[0]) == str:
                self.blockID += 1
            if script[0] == 'procDef':
                self.blockID += 1 + len(script[2])
            else:
                for block in script:
                    if type(block) == list:
                        self.getCommentBlockIDs(block)

    def convertTarget(self, target, index):

        sprite = {}

        sprite['objName'] = target['name']
        self.targetName = sprite['objName']
        scripts = []
        variables = []
        lists = []
        self.sounds = []
        self.costumes = []
        self.comments = []

        isStage = target['isStage']
        self.targetIsStage = isStage

        self.costumeName = False
        self.dragMode = False
        if not isStage:
            self.dragMode = target['draggable']
        self.penUpDown = False

        for s in target['sounds']:
            self.addSound(s)

        for c in target['costumes']:
            self.addCostume(c)

        for key, v in target['variables'].items():
            variable = {
                'name': self.varName(v[0]),
                'value': ProjectConverter.specialNum(v[1]),
                'isPersistent': len(v) >= 3 and v[2]
            }
            variables.append(variable)

        for key, l in target['lists'].items():
            ls = {
                'listName': self.varName(l[0]),
                'contents': [ProjectConverter.specialNum(item) for item in l[1]],
                'isPersistent': False
            }
            lists.append(ls)

        self.blockComments = {}

        for key, c in target['comments'].items():
            self.addComment(c)

        blocks = target['blocks']

        for key, b in blocks.items():
            if type(b) == dict:
                b['UID'] = key

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
                    script.append([['readVariable', self.varName(b[1])]])
                elif b[0] == 13:
                    script.append([['contentsOfList:', self.varName(b[1])]])
                else:
                    script = None

                if script != None:
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

        # Add variables, lists, and custom blocks for compatibility mode

        self.blockID = 0
        for script in scripts:
            self.getCommentBlockIDs(script[2])

        if self.compat:

            if False:
                lists.append({
                    'listName': self.compatVarName('results'),
                    'contents': [],
                    'isPersistent': False,
                    'visible': False
                })

            if self.costumeName:
                costumeNames = []
                for c in target['costumes']:
                    costumeNames.append(c['name'])
                lists.append({
                    'listName': self.compatVarName('costume names'),
                    'contents': costumeNames,
                    'isPersistent': False,
                    'visible': False
                })

            if self.penUpDown or self.dragMode:

                pen = self.compatVarName('pen')
                variables.append({
                    'name': pen,
                    'value': 'up',
                    'isPersistent': False
                })
                drag = self.compatVarName('drag')
                variables.append({
                    'name': drag,
                    'value': 'draggable' if (not isStage and target['draggable']) else 'not draggable',
                    'isPersistent': False
                })

                scripts.append(
                    [0,
					    0,
					    [["procDef", "pen down", [], [], True], ["putPenDown"], ["setVar:to:", pen, "down"]]]
                )
                scripts.append(
                    [0,
					    0,
					    [["procDef", "pen up", [], [], True], ["putPenUp"], ["setVar:to:", pen, "up"]]]
                )

                scripts.append(
                    [0,
                        0,
                        [["whenClicked"],
                            ["doIf",
                                ["=", ["readVariable", drag], "draggable"],
                                [["call",
                                        "drag %n %n",
                                        ["-", ["xpos"], ["mouseX"]],
                                        ["-", ["ypos"], ["mouseY"]]]]]]]
                )

                scripts.append(
                    [0,
                        0,
                        [["procDef", "set drag mode %s", ["drag"], [""], True],
                            ["setVar:to:", drag, ["getParam", "drag", "r"]]]]
                )

                scripts.append(
                    [0,
                        0,
                        [["procDef", "drag %n %n", ["X", "Y"], [0, 0], False],
                            ["doIf", ["=", ["readVariable", pen], "down"], [["putPenUp"]]],
                            ["doUntil",
                                ["not", ["mousePressed"]],
                                [["gotoX:y:",
                                        ["+", ["mouseX"], ["getParam", "X", "r"]],
                                        ["+", ["mouseY"], ["getParam", "Y", "r"]]]]],
                            ["doIf", ["=", ["readVariable", pen], "down"], [["putPenDown"]]]]]
                )

                self.scriptCount += 5

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
            sprite['penLayerMD5'] = ''

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
            sprite['isDraggable'] = target['draggable'] and not self.compat
            sprite['indexInLibrary'] = index
            sprite['visible'] = target['visible']
            sprite['spriteInfo'] = {}
            sprite['layerOrder'] = target['layerOrder']

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

        if m['opcode'] == 'data_listcontents':

            monitor = {
                'listName': self.varName(m['params']['LIST']),
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

            try:
                block = {'opcode': m['opcode']}
                if 'params' in m:
                    block['fields'] = {}
                    for key, value in m['params'].items():
                        block['fields'][key] = [value]

                monitor = self.argmapper.mapArgs(m['opcode'], block, {})
                cmd = 'getVar:' if monitor[0] == 'readVariable' else monitor[0]
                if len(monitor) > 1:
                    param = monitor[1]
                else:
                    param = None

                assert cmd != None

                sMin = m['min'] if 'min' in m else m['sliderMin']
                sMax = m['max'] if 'max' in m else m['sliderMax']
                monitor = {
                    'target': 'Stage' if m['spriteName'] == None else m['spriteName'],
                    'cmd': cmd,
                    'param': param,
                    'color': ProjectConverter.monitorColors[m['opcode'].split('_')[0]],
                    'label': '',  # Scratch 2 will handle this
                    'mode': ProjectConverter.varModes[m['mode']],
                    'sliderMin': sMin,
                    'sliderMax': sMax,
                    'isDiscrete': sMin % 1 == 0 and sMax % 1 == 0 and not ('.' in str(sMin)) and not ('.' in str(sMax)),
                    'x': m['x'],
                    'y': m['y'],
                    'visible': m['visible']
                }
                self.monitors.append(monitor)

            except:
                self.generateWarning("Stage monitor '{}' will not be converted".format(m['opcode']))

    def convertProject(self, sb3path, sb2path, replace=False, compatibility=False):
        
        self.compat = compatibility
        self.warnings = 0

        if not sb3path[-3:] == 'sb3':
            printError("File '{}' is not an sb3 file".format(sb3path))

        if not sb2path[-3:] == 'sb2':
            self.generateWarning("The converted project will be saved to '{}' instead of '{}'".format(sb2path + '.sb2', sb2path))
            sb2path += '.sb2'

        self.convertingMonitors = False

        try:
            self.zfsb3 = zipfile.ZipFile(sb3path, 'r')
        except:
            printError("File '{}' does not exist".format(sb3path))

        try:
            self.zfsb2 = zipfile.ZipFile(sb2path, 'x')
        except:
            replaceFile = False
            if replace:
                replaceFile = True
            else:
                print("File '{}' already exists".format(sb2path))
                replaceFile = input("Overwrite '{}'? (Y/N): ".format(sb2path))
                replaceFile = replaceFile == 'Y' or replaceFile == 'y'
            if replaceFile:
                import os
                os.remove(sb2path)
                self.zfsb2 = zipfile.ZipFile(sb2path, 'x')
            else:
                exit()

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

        self.convertingMonitors = True
        for m in self.jsonData['monitors']:
            self.addMonitor(m)

        self.updateListData(output, sprites, self.lists)

        # Sort sprites into their layers

        sprites.sort(key = lambda sprite: sprite['layerOrder'])
        for sprite in sprites:
            del sprite['layerOrder']

        sprites.extend(self.monitors)
        self.convertingMonitors = False

        output['children'] = sprites

        # Add WeDo 2.0 extension if necessary

        if 'wedo2' in self.jsonData['extensions']:
            output['info']['savedExtensions'] = [{'extensionName': 'LEGO WeDo 2.0'}]

        output = json.dumps(output)

        self.zfsb2.writestr('project.json', output)

        return (self.warnings, sb2path)

if __name__ == '__main__':

    dialog = False
    if len(sys.argv) < 3:
        dialog = True
        import tkinter
        from tkinter import filedialog

        root = tkinter.Tk()
        root.withdraw()
        sb3path = filedialog.askopenfilename(title="Open SB3 Project", filetypes=[("Scratch 3 Project", "*.sb3")])
        sb2path = filedialog.asksaveasfilename(title="Save as SB2 Project", filetypes=[("Scratch 2 Project", "*.sb2")])
    else:
        sb3path = sys.argv[-2]
        sb2path = sys.argv[-1]

    args = []
    if len(sys.argv) > 3:
        for arg in sys.argv[1:-2]:
            args.append(arg)

    result = ProjectConverter().convertProject(sb3path, sb2path, replace=dialog, compatibility=('-c' in args))
    warnings = result[0]
    sb2path = result[1]

    if warnings == 0:
        print('Saved to {} with no warnings'.format(sb2path))
    elif warnings == 1:
        print('Saved to {} with {} warning'.format(sb2path, warnings))
    else:
        print('Saved to {} with {} warnings'.format(sb2path, warnings))