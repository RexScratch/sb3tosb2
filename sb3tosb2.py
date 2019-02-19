import sys, json, zipfile

class Blocks:

    # Motion

    @staticmethod
    def motion_movesteps(block, blocks):
        output = ['forward:']
        output.append(inputVal('STEPS', block, blocks))
        return output

    @staticmethod
    def motion_turnright(block, blocks):
        output = ['turnRight:']
        output.append(inputVal('DEGREES', block, blocks))
        return output

    @staticmethod
    def motion_turnleft(block, blocks):
        output = ['turnLeft:']
        output.append(inputVal('DEGREES', block, blocks))
        return output

    @staticmethod
    def motion_pointindirection(block, blocks):
        output = ['heading:']
        output.append(inputVal('DIRECTION', block, blocks))
        return output

    @staticmethod
    def motion_pointtowards(block, blocks):
        output = ['pointTowards:']
        output.append(inputVal('TOWARDS', block, blocks))
        return output

    @staticmethod
    def motion_gotoxy(block, blocks):
        output = ['gotoX:y:']
        output.append(inputVal('X', block, blocks))
        output.append(inputVal('Y', block, blocks))
        return output

    @staticmethod
    def motion_goto(block, blocks):
        output = ['gotoSpriteOrMouse:']
        output.append(inputVal('TO', block, blocks))
        return output

    @staticmethod
    def motion_glidesecstoxy(block, blocks):
        output = ['glideSecs:toX:y:elapsed:from:']
        output.append(inputVal('SECS', block, blocks))
        output.append(inputVal('X', block, blocks))
        output.append(inputVal('Y', block, blocks))
        return output

    @staticmethod
    def motion_changexby(block, blocks):
        output = ['changeXposBy:']
        output.append(inputVal('DX', block, blocks))
        return output

    @staticmethod
    def motion_setx(block, blocks):
        output = ['xpos:']
        output.append(inputVal('X', block, blocks))
        return output

    @staticmethod
    def motion_changeyby(block, blocks):
        output = ['changeYposBy:']
        output.append(inputVal('DY', block, blocks))
        return output

    @staticmethod
    def motion_sety(block, blocks):
        output = ['ypos:']
        output.append(inputVal('Y', block, blocks))
        return output

    @staticmethod
    def motion_ifonedgebounce(block, blocks):
        return ['bounceOffEdge']

    @staticmethod
    def motion_setrotationstyle(block, blocks):
        output = ['setRotationStyle']
        output.append(fieldVal('STYLE', block))
        return output

    @staticmethod
    def motion_xposition(block, blocks):
        return ['xpos']

    @staticmethod
    def motion_yposition(block, blocks):
        return ['ypos']

    @staticmethod
    def motion_direction(block, blocks):
        return ['heading']

    @staticmethod
    def motion_scroll_right(block, blocks):
        output = ['scrollRight']
        output.append(inputVal('DISTANCE', block, blocks))
        return output
    
    @staticmethod
    def motion_scroll_up(block, blocks):
        output = ['scrollUp']
        output.append(inputVal('DISTANCE', block, blocks))
        return output

    @staticmethod
    def motion_align_scene(block, blocks):
        output = ['scrollAlign']
        output.append(fieldVal('ALIGNMENT', block))
        return output

    @staticmethod
    def motion_xscroll(block, blocks):
        return ['xScroll']

    @staticmethod
    def motion_yscroll(block, blocks):
        return ['yScroll']
    
    # Looks

    @staticmethod
    def looks_sayforsecs(block, blocks):
        output = ['say:duration:elapsed:from:']
        output.append(inputVal('MESSAGE', block, blocks))
        output.append(inputVal('SECS', block, blocks))
        return output

    @staticmethod
    def looks_say(block, blocks):
        output = ['say:']
        output.append(inputVal('MESSAGE', block, blocks))
        return output

    @staticmethod
    def looks_thinkforsecs(block, blocks):
        output = ['think:duration:elapsed:from:']
        output.append(inputVal('MESSAGE', block, blocks))
        output.append(inputVal('SECS', block, blocks))
        return output

    @staticmethod
    def looks_think(block, blocks):
        output = ['think:']
        output.append(inputVal('MESSAGE', block, blocks))
        return output

    @staticmethod
    def looks_show(block, blocks):
        return ['show']

    @staticmethod
    def looks_hide(block, blocks):
        return ['hide']

    @staticmethod
    def looks_hideallsprites(block, blocks):
        return ['hideAll']

    @staticmethod
    def looks_switchcostumeto(block, blocks):
        output = ['lookLike:']
        output.append(inputVal('COSTUME', block, blocks))
        return output

    @staticmethod
    def looks_nextcostume(block, blocks):
        return ['nextCostume']
    
    @staticmethod
    def looks_switchbackdropto(block, blocks):
        output = ['startScene']
        output.append(inputVal('BACKDROP', block, blocks))
        return output

    @staticmethod
    def looks_changeeffectby(block, blocks):
        output = ['changeGraphicEffect:by:']
        field = fieldVal('EFFECT', block)
        if type(field) == str:
            field = str.lower(field)
        output.append(field)
        output.append(inputVal('CHANGE', block, blocks))
        return output

    @staticmethod
    def looks_seteffectto(block, blocks):
        output = ['setGraphicEffect:to:']
        field = fieldVal('EFFECT', block)
        if type(field) == str:
            field = str.lower(field)
        output.append(field)
        output.append(inputVal('VALUE', block, blocks))
        return output
    
    @staticmethod
    def looks_cleargraphiceffects(block, blocks):
        return ['filterReset']

    @staticmethod
    def looks_changesizeby(block, blocks):
        output = ['changeSizeBy:']
        output.append(inputVal('CHANGE', block, blocks))
        return output

    @staticmethod
    def looks_setsizeto(block, blocks):
        output = ['setSizeTo:']
        output.append(inputVal('SIZE', block, blocks))
        return output

    @staticmethod
    def looks_changestretchby(block, blocks):
        output = ['changeStretchBy:']
        output.append(inputVal('CHANGE', block, blocks))
        return output

    @staticmethod
    def looks_setstretchto(block, blocks):
        output = ['setStretchTo:']
        output.append(inputVal('STRETCH', block, blocks))
        return output

    @staticmethod
    def looks_gotofrontback(block, blocks):
        field = fieldVal('FRONT_BACK', block)
        if field == 'front':
            return ['comeToFront']
        else:
            printWarn("Incompatible block 'go to [back v] layer' will be converted to 'go back (1.79e+308) layers'")
            return ['goBackByLayers:', 1.79e+308]

    @staticmethod
    def looks_goforwardbackwardlayers(block, blocks):
        layers = inputVal('NUM', block, blocks)
        field = fieldVal('FORWARD', block)
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

    @staticmethod
    def looks_costumenumbername(block, blocks):
        field = fieldVal('NUMBER_NAME', block)
        if field == 'number':
            return ['costumeIndex']
        elif field == 'name':
            printWarn("Incompatible block 'costume [name v]")
            return ['costumeName']

    @staticmethod
    def looks_backdropnumbername(block, blocks):
        field = fieldVal('NUMBER_NAME', block)
        if field == 'number':
            return ['backgroundIndex']
        elif field == 'name':
            return ['sceneName']

    @staticmethod
    def looks_size(block, blocks):
        return ['scale']

    @staticmethod
    def looks_switchbackdroptoandwait(block, blocks):
        output = ['startSceneAndWait']
        output.append(inputVal('BACKDROP', block, blocks))
        return output

    @staticmethod
    def looks_nextbackdrop(block, blocks):
        return ['nextScene']

    # Sound

    @staticmethod
    def sound_play(block, blocks):
        output = ['playSound:']
        output.append(inputVal('SOUND_MENU', block, blocks))
        return output
    
    @staticmethod
    def sound_playuntildone(block, blocks):
        output = ['doPlaySoundAndWait']
        output.append(inputVal('SOUND_MENU', block, blocks))
        return output

    @staticmethod
    def sound_stopallsounds(block, blocks):
        return ['stopAllSounds']
    
    @staticmethod
    def sound_changevolumeby(block, blocks):
        output = ['changeVolumeBy:']
        output.append(inputVal('VOLUME', block, blocks))
        return output

    @staticmethod
    def sound_setvolumeto(block, blocks):
        output = ['setVolumeTo:']
        output.append(inputVal('VOLUME', block, blocks))
        return output

    @staticmethod
    def sound_volume(block, blocks):
        return ['volume']

    # Music

    @staticmethod
    def music_playDrumForBeats(block, blocks):
        output = ['playDrum']
        output.append(inputVal('DRUM', block, blocks))
        output.append(inputVal('BEATS', block, blocks))
        return output

    @staticmethod
    def music_midiPlayDrumForBeats(block, blocks):
        output = ['drum:duration:elapsed:from:']
        output.append(inputVal('DRUM', block, blocks))
        output.append(inputVal('BEATS', block, blocks))
        return output

    @staticmethod
    def music_restForBeats(block, blocks):
        output = ['rest:elapsed:from:']
        output.append(inputVal('BEATS', block, blocks))
        return output

    @staticmethod
    def music_playNoteForBeats(block, blocks):
        output = ['noteOn:duration:elapsed:from:']
        output.append(inputVal('NOTE', block, blocks))
        output.append(inputVal('BEATS', block, blocks))
        return output

    @staticmethod
    def music_setInstrument(block, blocks):
        output = ['instrument:']
        output.append(inputVal('INSTRUMENT', block, blocks))
        return output

    @staticmethod
    def music_midiSetInstrument(block, blocks):
        output = ['midiInstrument:']
        output.append(inputVal('INSTRUMENT', block, blocks))
        return output

    @staticmethod
    def music_changeTempo(block, blocks):
        output = ['changeTempoBy:']
        output.append(inputVal('TEMPO', block, blocks))
        return output

    @staticmethod
    def music_setTempo(block, blocks):
        output = ['setTempoTo:']
        output.append(inputVal('TEMPO', block, blocks))
        return output

    @staticmethod
    def music_getTempo(block, blocks):
        return ['tempo']

    # Pen

    @staticmethod
    def pen_clear(block, blocks):
        return ['clearPenTrails']

    @staticmethod
    def pen_stamp(block, blocks):
        return ['stampCostume']

    @staticmethod
    def pen_penDown(block, blocks):
        return ['putPenDown']

    @staticmethod
    def pen_penUp(block, blocks):
        return ['putPenUp']

    @staticmethod
    def pen_setPenColorToColor(block, blocks):
        output = ['penColor:']
        output.append(inputVal('COLOR', block, blocks))
        return output

    @staticmethod
    def pen_changePenHueBy(block, blocks):
        output = ['changePenHueBy:']
        output.append(inputVal('HUE', block, blocks))
        return output

    @staticmethod
    def pen_setPenHueToNumber(block, blocks):
        output = ['setPenHueTo:']
        output.append(inputVal('HUE', block, blocks))
        return output

    @staticmethod
    def pen_changePenShadeBy(block, blocks):
        output = ['changePenShadeBy:']
        output.append(inputVal('SHADE', block, blocks))
        return output

    @staticmethod
    def pen_setPenShadeToNumber(block, blocks):
        output = ['setPenShadeTo:']
        output.append(inputVal('SHADE', block, blocks))
        return output

    @staticmethod
    def pen_changePenSizeBy(block, blocks):
        output = ['changePenSizeBy:']
        output.append(inputVal('SIZE', block, blocks))
        return output

    @staticmethod
    def pen_setPenSizeTo(block, blocks):
        output = ['penSize:']
        output.append(inputVal('SIZE', block, blocks))
        return output

    @staticmethod
    def pen_setPenColorParamTo(block, blocks):
        param = inputVal('COLOR_PARAM', block, blocks)
        value = inputVal('VALUE', block, blocks)
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
            printWarn("Incompatible block 'set pen [{} v] to ({})'".format(param, value))
            return ['pen_setPenColorParamTo', value, param]

    @staticmethod
    def pen_changePenColorParamBy(block, blocks):
        param = inputVal('COLOR_PARAM', block, blocks)
        value = inputVal('VALUE', block, blocks)
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
            printWarn("Incompatible block 'change pen [{} v] by ({})'".format(param, value))
            return ['pen_changeColorParamBy', value, param]

    # Events

    @staticmethod
    def event_whenflagclicked(block, blocks):
        return ['whenGreenFlag']

    @staticmethod
    def event_whenkeypressed(block, blocks):
        output = ['whenKeyPressed']
        output.append(fieldVal('KEY_OPTION', block))
        return output

    @staticmethod
    def event_whenthisspriteclicked(block, blocks):
        return ['whenClicked']

    @staticmethod
    def event_whenbackdropswitchesto(block, blocks):
        output = ['whenSceneStarts']
        output.append(fieldVal('BACKDROP', block))
        return output

    @staticmethod
    def event_whengreaterthan(block, blocks):
        output = ['whenSensorGreaterThan']
        field = fieldVal('WHENGREATERTHANMENU', block)
        if type(field) == str:
            field = str.lower(field)
        output.append(field)
        output.append(inputVal('VALUE', block, blocks))
        return output
    
    @staticmethod
    def event_whenbroadcastreceived(block, blocks):
        output = ['whenIReceive']
        output.append(fieldVal('BROADCAST_OPTION', block))
        return output
    
    @staticmethod
    def event_broadcast(block, blocks):
        output = ['broadcast:']
        output.append(inputVal('BROADCAST_INPUT', block, blocks))
        return output

    @staticmethod
    def event_broadcastandwait(block, blocks):
        output = ['doBroadcastAndWait']
        output.append(inputVal('BROADCAST_INPUT', block, blocks))
        return output

    # Control

    @staticmethod
    def control_wait(block, blocks):
        output = ['wait:elapsed:from:']
        output.append(inputVal('DURATION', block, blocks))
        return output
    
    @staticmethod
    def control_repeat(block, blocks):
        output = ['doRepeat']
        output.append(inputVal('TIMES', block, blocks))
        output.append(substack('SUBSTACK', block, blocks))
        return output
    
    @staticmethod
    def control_forever(block, blocks):
        output = ['doForever']
        output.append(substack('SUBSTACK', block, blocks))
        return output
    
    @staticmethod
    def control_if(block, blocks):
        output = ['doIf']
        output.append(inputVal('CONDITION', block, blocks))
        output.append(substack('SUBSTACK', block, blocks))
        return output

    @staticmethod
    def control_if_else(block, blocks):
        output = ['doIfElse']
        output.append(inputVal('CONDITION', block, blocks))
        output.append(substack('SUBSTACK', block, blocks))
        output.append(substack('SUBSTACK2', block, blocks))
        return output

    @staticmethod
    def control_wait_until(block, blocks):
        output = ['doWaitUntil']
        output.append(inputVal('CONDITION', block, blocks))
        return output

    @staticmethod
    def control_repeat_until(block, blocks):
        output = ['doUntil']
        output.append(inputVal('CONDITION', block, blocks))
        output.append(substack('SUBSTACK', block, blocks))
        return output

    @staticmethod
    def control_while(block, blocks):
        output = ['doWhile']
        output.append(inputVal('CONDITION', block, blocks))
        output.append(substack('SUBSTACK', block, blocks))
        return output

    @staticmethod
    def control_for_each(block, blocks):
        output = ['doForLoop']
        output.append(fieldVal('VARIABLE', block))
        output.append(inputVal('VALUE', block, blocks))
        output.append(substack('SUBSTACK', block, blocks))
        return output
    
    @staticmethod
    def control_stop(block, blocks):
        output = ['stopScripts']
        output.append(fieldVal('STOP_OPTION', block))
        return output
    
    @staticmethod
    def control_start_as_clone(block, blocks):
        return ['whenCloned']

    @staticmethod
    def control_create_clone_of(block, blocks):
        output = ['createCloneOf']
        output.append(inputVal('CLONE_OPTION', block, blocks))
        return output
    
    @staticmethod
    def control_delete_this_clone(block, blocks):
        return ['deleteClone']

    @staticmethod
    def control_get_counter(block, blocks):
        return ['COUNT']

    @staticmethod
    def control_incr_counter(block, blocks):
        return ['INCR_COUNT']

    @staticmethod
    def control_clear_counter(block, blocks):
        return ['CLR_COUNT']

    @staticmethod
    def control_all_at_once(block, blocks):
        output = ['warpSpeed']
        output.append(substack('SUBSTACK', block, blocks))
        return output

    # Video Sensing

    @staticmethod
    def videoSensing_videoOn(block, blocks):
        output = ['senseVideoMotion']
        output.append(inputVal('ATTRIBUTE', block, blocks))
        output.append(inputVal('SUBJECT', block, blocks))
        return output

    @staticmethod
    def videoSensing_whenMotionGreaterThan(block, blocks):
        output = ['whenSensorGreaterThan', 'video motion']
        output.append(inputVal('REFERENCE', block, blocks))
        return output

    @staticmethod
    def videoSensing_videoToggle(block, blocks):
        output = ['setVideoState']
        output.append(inputVal('VIDEO_STATE', block, blocks))
        return output

    @staticmethod
    def videoSensing_setVideoTransparency(block, blocks):
        output = ['setVideoTransparency']
        output.append(inputVal('TRANSPARENCY', block, blocks))
        return output

    # Sensing

    @staticmethod
    def sensing_touchingobject(block, blocks):
        output = ['touching:']
        output.append(inputVal('TOUCHINGOBJECTMENU', block, blocks))
        return output

    @staticmethod
    def sensing_touchingcolor(block, blocks):
        output = ['touchingColor:']
        output.append(inputVal('COLOR', block, blocks))
        return output

    @staticmethod
    def sensing_coloristouchingcolor(block, blocks):
        output = ['color:sees:']
        output.append(inputVal('COLOR', block, blocks))
        output.append(inputVal('COLOR2', block, blocks))
        return output

    @staticmethod
    def sensing_distanceto(block, blocks):
        output = ['distanceTo:']
        output.append(inputVal('DISTANCETOMENU', block, blocks))
        return output

    @staticmethod
    def sensing_askandwait(block, blocks):
        output = ['doAsk']
        output.append(inputVal('QUESTION', block, blocks))
        return output

    @staticmethod
    def sensing_answer(block, blocks):
        return ['answer']

    @staticmethod
    def sensing_keypressed(block, blocks):
        output = ['keyPressed:']
        output.append(inputVal('KEY_OPTION', block, blocks))
        return output

    @staticmethod
    def sensing_mousedown(block, blocks):
        return ['mousePressed']

    @staticmethod
    def sensing_mousex(block, blocks):
        return ['mouseX']

    @staticmethod
    def sensing_mousey(block, blocks):
        return ['mouseY']

    @staticmethod
    def sensing_loudness(block, blocks):
        return ['soundLevel']

    @staticmethod
    def sensing_loud(block, blocks):
        return ['isLoud']

    @staticmethod
    def sensing_timer(block, blocks):
        return ['timer']

    @staticmethod
    def sensing_resettimer(block, blocks):
        return ['timerReset']

    @staticmethod
    def sensing_of(block, blocks):
        output = ['getAttribute:of:']
        output.append(fieldVal('PROPERTY', block))
        output.append(inputVal('OBJECT', block, blocks))
        return output

    @staticmethod
    def sensing_current(block, blocks):
        output = ['timeAndDate']
        field = fieldVal('CURRENTMENU', block)
        if type(field) == str:
            field = str.lower(field)
        output.append(field)
        return output

    @staticmethod
    def sensing_dayssince2000(block, blocks):
        return ['timestamp']

    @staticmethod
    def sensing_username(block, blocks):
        return ['getUserName']

    @staticmethod
    def sensing_userid(block, blocks):
        return ['getUserId']

    # Operators

    @staticmethod
    def operator_add(block, blocks):
        output = ['+']
        output.append(inputVal('NUM1', block, blocks))
        output.append(inputVal('NUM2', block, blocks))
        return output

    @staticmethod   
    def operator_subtract(block, blocks):
        output = ['-']
        output.append(inputVal('NUM1', block, blocks))
        output.append(inputVal('NUM2', block, blocks))
        return output

    @staticmethod
    def operator_multiply(block, blocks):
        output = ['*']
        output.append(inputVal('NUM1', block, blocks))
        output.append(inputVal('NUM2', block, blocks))
        return output

    @staticmethod
    def operator_divide(block, blocks):
        output = ['/']
        output.append(inputVal('NUM1', block, blocks))
        output.append(inputVal('NUM2', block, blocks))
        return output

    @staticmethod
    def operator_random(block, blocks):
        output = ['randomFrom:to:']
        output.append(inputVal('FROM', block, blocks))
        output.append(inputVal('TO', block, blocks))
        return output

    @staticmethod
    def operator_gt(block, blocks):
        output = ['>']
        output.append(inputVal('OPERAND1', block, blocks))
        output.append(inputVal('OPERAND2', block, blocks))
        return output
    
    @staticmethod
    def operator_lt(block, blocks):
        output = ['<']
        output.append(inputVal('OPERAND1', block, blocks))
        output.append(inputVal('OPERAND2', block, blocks))
        return output
    
    @staticmethod
    def operator_equals(block, blocks):
        output = ['=']
        output.append(inputVal('OPERAND1', block, blocks))
        output.append(inputVal('OPERAND2', block, blocks))
        return output

    @staticmethod
    def operator_and(block, blocks):
        output = ['&']
        output.append(inputVal('OPERAND1', block, blocks))
        output.append(inputVal('OPERAND2', block, blocks))
        return output

    @staticmethod
    def operator_or(block, blocks):
        output = ['|']
        output.append(inputVal('OPERAND1', block, blocks))
        output.append(inputVal('OPERAND2', block, blocks))
        return output

    @staticmethod
    def operator_not(block, blocks):
        output = ['not']
        output.append(inputVal('OPERAND', block, blocks))
        return output

    @staticmethod
    def operator_join(block, blocks):
        output = ['concatenate:with:']
        output.append(inputVal('STRING1', block, blocks))
        output.append(inputVal('STRING2', block, blocks))
        return output

    @staticmethod
    def operator_letter_of(block, blocks):
        output = ['letter:of:']
        output.append(inputVal('LETTER', block, blocks))
        output.append(inputVal('STRING', block, blocks))
        return output

    @staticmethod
    def operator_length(block, blocks):
        output = ['stringLength:']
        output.append(inputVal('STRING', block, blocks))
        return output

    @staticmethod
    def operator_mod(block, blocks):
        output = ['%']
        output.append(inputVal('NUM1', block, blocks))
        output.append(inputVal('NUM2', block, blocks))
        return output

    @staticmethod
    def operator_round(block, blocks):
        output = ['rounded']
        output.append(inputVal('NUM', block, blocks))
        return output
    
    @staticmethod
    def operator_mathop(block, blocks):
        output = ['computeFunction:of:']
        output.append(fieldVal('OPERATOR', block))
        output.append(inputVal('NUM', block, blocks))
        return output

    # Data

    @staticmethod
    def data_variable(block, blocks):
        output = ['readVariable']
        output.append(fieldVal('VARIABLE', block))
        return output   

    @staticmethod
    def data_setvariableto(block, blocks):
        output = ['setVar:to:']
        output.append(fieldVal('VARIABLE', block))
        output.append(inputVal('VALUE', block, blocks))
        return output

    @staticmethod
    def data_changevariableby(block, blocks):
        output = ['changeVar:by:']
        output.append(fieldVal('VARIABLE', block))
        output.append(inputVal('VALUE', block, blocks))
        return output

    @staticmethod
    def data_showvariable(block, blocks):
        output = ['showVariable:']
        output.append(fieldVal('VARIABLE', block))
        return output

    @staticmethod
    def data_hidevariable(block, blocks):
        output = ['hideVariable:']
        output.append(fieldVal('VARIABLE', block))
        return output

    @staticmethod
    def data_listcontents(block, blocks):
        output = ['contentsOfList:']
        output.append(fieldVal('LIST', block))
        return output
    
    @staticmethod
    def data_addtolist(block, blocks):
        output = ['append:toList:']
        output.append(inputVal('ITEM', block, blocks))
        output.append(fieldVal('LIST', block))
        return output

    @staticmethod
    def data_deleteoflist(block, blocks):
        output = ['deleteLine:ofList:']
        output.append(inputVal('INDEX', block, blocks))
        output.append(fieldVal('LIST', block))
        return output
    
    @staticmethod
    def data_deletealloflist(block, blocks):
        output = ['deleteLine:ofList:', 'all']
        output.append(fieldVal('LIST', block))
        return output

    @staticmethod
    def data_insertatlist(block, blocks):
        output = ['insert:at:ofList:']
        output.append(inputVal('ITEM', block, blocks))
        output.append(inputVal('INDEX', block, blocks))
        output.append(fieldVal('LIST', block))
        return output

    @staticmethod
    def data_replaceitemoflist(block, blocks):
        output = ['setLine:ofList:to:']
        output.append(inputVal('INDEX', block, blocks))
        output.append(fieldVal('LIST', block))
        output.append(inputVal('ITEM', block, blocks))
        return output

    @staticmethod
    def data_itemoflist(block, blocks):
        output = ['getLine:ofList:']
        output.append(inputVal('INDEX', block, blocks))
        output.append(fieldVal('LIST', block))
        return output

    @staticmethod
    def data_lengthoflist(block, blocks):
        output = ['lineCountOfList:']
        output.append(fieldVal('LIST', block))
        return output

    @staticmethod
    def data_listcontainsitem(block, blocks):
        output = ['list:contains:']
        output.append(fieldVal('LIST', block))
        output.append(inputVal('ITEM', block, blocks))
        return output

    @staticmethod
    def data_showlist(block, blocks):
        output = ['showList:']
        output.append(fieldVal('LIST', block))
        return output

    @staticmethod
    def data_hidelist(block, blocks):
        output = ['hideList:']
        output.append(fieldVal('LIST', block))
        return output

    # Procedures

    @staticmethod
    def procedures_definition(block, blocks):
        global blockID
        block = blocks[block['inputs']['custom_block'][1]]
        procData = block['mutation']
        output = ['procDef']
        output.append(procData['proccode'])
        output.append(json.loads(procData['argumentnames']))
        output.append(json.loads(procData['argumentdefaults']))
        blockID += (1 + len(output[-2]))
        if len(output[-1]) != len(output[-2]):
            output[-1] = len(output[-2]) * ['']
        warp = procData['warp']
        output.append(warp == 'true' or (type(warp) == bool and warp))
        return output

    @staticmethod
    def procedures_call(block, blocks):
        output = ['call']
        output.append(block['mutation']['proccode'])
        ids = json.loads(block['mutation']['argumentids'])
        for i in ids:
            output.append(inputVal(i, block, blocks))
        return output

    @staticmethod
    def argument_reporter_string_number(block, blocks):
        output = ['getParam']
        output.append(fieldVal('VALUE', block))
        output.append('r')
        return output

    @staticmethod
    def argument_reporter_boolean(block, blocks):
        output = ['getParam']
        output.append(fieldVal('VALUE', block))
        output.append('b')
        return output

    # LEGO WeDo 2.0

    @staticmethod
    def wedo2_motorOnFor(block, blocks):
        output = ['LEGO WeDo 2.0\u001fmotorOnFor']
        output.append(inputVal('MOTOR_ID', block, blocks))
        output.append(inputVal('DURATION', block, blocks))
        return output

    @staticmethod
    def wedo2_motorOn(block, blocks):
        output = ['LEGO WeDo 2.0\u001fmotorOn']
        output.append(inputVal('MOTOR_ID', block, blocks))
        return output

    @staticmethod
    def wedo2_motorOff(block, blocks):
        output = ['LEGO WeDo 2.0\u001fmotorOff']
        output.append(inputVal('MOTOR_ID', block, blocks))
        return output
    
    @staticmethod
    def wedo2_startMotorPower(block, blocks):
        output = ['LEGO WeDo 2.0\u001fstartMotorPower']
        output.append(inputVal('MOTOR_ID', block, blocks))
        output.append(inputVal('POWER', block, blocks))
        return output

    @staticmethod
    def wedo2_setMotorDirection(block, blocks):
        output = ['LEGO WeDo 2.0\u001fsetMotorDirection']
        output.append(inputVal('MOTOR_ID', block, blocks))
        output.append(inputVal('MOTOR_DIRECTION', block, blocks))
        return output

    @staticmethod
    def wedo2_setLightHue(block, blocks):
        output = ['LEGO WeDo 2.0\u001fsetLED']
        output.append(inputVal('HUE', block, blocks))
        return output

    @staticmethod
    def wedo2_playNoteFor(block, blocks):
        output = ['LEGO WeDo 2.0\u001fplayNote']
        output.append(inputVal('NOTE', block, blocks))
        output.append(inputVal('DURATION', block, blocks))
        return output

    @staticmethod
    def wedo2_whenDistance(block, blocks):
        output = ['LEGO WeDo 2.0\u001fwhenDistance']
        output.append(inputVal('OP', block, blocks))
        output.append(inputVal('REFERENCE', block, blocks))
        return output

    @staticmethod
    def wedo2_whenTilted(block, blocks):
        output = ['LEGO WeDo 2.0\u001fwhenTilted']
        output.append(inputVal('TILT_DIRECTION_ANY', block, blocks))
        return output

    @staticmethod
    def wedo2_getDistance(block, blocks):
        return ['LEGO WeDo 2.0\u001fgetDistance']

    @staticmethod
    def wedo2_isTilted(block, blocks):
        output = ['LEGO WeDo 2.0\u001fisTilted']
        output.append(inputVal('TILT_DIRECTION_ANY', block, blocks))
        return output

    @staticmethod
    def wedo2_getTiltAngle(block, blocks):
        output = ['LEGO WeDo 2.0\u001fgetTilt']
        output.append(inputVal('TILT_DIRECTION', block, blocks))
        return output

Blocks.funcs = {}
funcTuples = [(name, obj) for name, obj in Blocks.__dict__.items() if type(obj) == staticmethod and not name.startswith('__')]

for name, obj in funcTuples:
    Blocks.funcs[name] = obj.__get__(object)

warnings = 0
blockID = 0

def printWarn(message):
    global warnings
    print("WARNING: " + message)
    warnings += 1

def setCommentBlockId(id):
    global blockID, comments, blockComments
    if id in blockComments:
        comments[blockComments[id]][5] = blockID

def hexToDec(hexNum):
    try:
        return int(hexNum[1:], 16)
    except:
        return hexNum

def hackedReporterBlockID(reporter):
    global blockID
    blockID += 1
    for value in reporter:
        if type(value) == list:
            hackedReporterBlockID(value)

def convert(block, blocks):
    global blockID
    opcode = block['opcode']
    if opcode in Blocks.funcs:
        blockID += 1
        return Blocks.funcs[opcode](block, blocks)
    elif len(block['inputs']) == 0 and len(block['fields']) == 1 and block['shadow']: # Menu opcodes and shadows
        return fieldVal(list(block['fields'].items())[0][0], block)
    else:
        blockID += 1
        printWarn("Incompatible opcode '{}'".format(opcode))
        
        output = [opcode]
        for i in block['inputs']:
            output.append(inputVal(i, block, blocks))
        for f in block['fields']:
            output.append(fieldVal(f, block))
        return output

def inputVal(value, block, blocks):
    global blockID

    if not value in block['inputs']:
        return False

    value = block['inputs'][value]
    if value[1] == None:
        return None
    if value[0] == 1:
        if type(value[1]) == str:
            setCommentBlockId(value[1])
            return convert(blocks[value[1]], blocks)
        else:
            output = value[1][1]        
    else:
        out = value[1]
        if type(out) == str:
            setCommentBlockId(out)
            return convert(blocks[out], blocks)
        else:
            if out[0] == 12:
                blockID += 1
                return ['readVariable', out[1]]
            elif out[0] == 13:
                blockID += 1
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
        output = hexToDec(output)

    if output == '-Infinity':
        output = float('-inf')
    elif output == 'Infinity':
        output = float('inf')
    elif output == 'NaN':
        output = float('nan')

    return output

def fieldVal(value, block):

    if not value in block['fields']:
        return None

    value = block['fields'][value][0]
    if type(value) == list:
        hackedReporterBlockID(value)

    return value

def substack(stack, block, blocks):

    if not stack in block['inputs']:
        return None

    stack = block['inputs'][stack]
    if len(stack) < 2 or stack[1] == None:
        return []

    setCommentBlockId(stack[1])
    block = blocks[stack[1]]
    script = []
    end = False
    while not end:
        script.append(convert(block, blocks))
        if block['next'] == None:
            end = True
        else:
            setCommentBlockId(block['next'])
            block = blocks[block['next']]
    return script

sb2path = sys.argv[2]

error = False
try:
    open(sb2path, 'r').close()
    print("ERROR: File '{}' already exists".format(sb2path))
    error = True
except:
    pass

if error:
    sys.exit()

zfsb2 = zipfile.ZipFile(sb2path, 'x')

sb3path = sys.argv[1]
zfsb3 = zipfile.ZipFile(sb3path, 'r')

f = zfsb3.open('project.json', 'r')
data = json.loads(f.read())
f.close()

output = {}
costumeAssets = {}
soundAssets = {}

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

sprites = []

targetsDone = 0
totalTargets = len(data['targets'])

scriptCount = 0

for target in data['targets']:

    sprite = {}
    sprite['objName'] = target['name']
    scripts = []
    variables = []
    lists = []
    sounds = []
    costumes = []
    comments = []

    isStage = target['isStage']

    for s in target['sounds']:
        if not s['assetId'] in soundAssets:
            soundAssets[s['assetId']] = len(soundAssets)
            if s['dataFormat'] == 'wav':
                f = zfsb3.open(s['md5ext'], 'r')
                zfsb2.writestr('{}.{}'.format(len(soundAssets) - 1, s['dataFormat']), bytes(f.read()))
                f.close()
            else:
                printWarn("Audio file '{}' cannot be converted into WAV".format(s['md5ext']))
        
        sound = {
            'soundName': s['name'],
            'soundID': soundAssets[s['assetId']],
            'md5': s['assetId'] + '.wav',
            'sampleCount': s['sampleCount'],
            'rate': s['rate'],
            'format': 'adpcm'
        }

        sounds.append(sound)

    for c in target['costumes']:
        if not c['assetId'] in costumeAssets:
            costumeAssets[c['assetId']] = len(costumeAssets)

            f = zfsb3.open(c['md5ext'], 'r')
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
            zfsb2.writestr('{}.{}'.format(len(costumeAssets) - 1, c['dataFormat']), img)
            f.close()

        costume = {
            'costumeName': c['name'],
            'baseLayerID': costumeAssets[c['assetId']],
            'baseLayerMD5': c['md5ext'],
            'rotationCenterX': c['rotationCenterX'],
            'rotationCenterY': c['rotationCenterY']
        }

        if 'bitmapResolution' in c:
            costume['bitmapResolution'] = c['bitmapResolution']

        costumes.append(costume)

    for key, v in target['variables'].items():
        variable = {
            'name': v[0],
            'value': v[1],
            'isPersistent': len(v) >= 3 and v[2]
        }
        variables.append(variable)

    for key, l in target['lists'].items():
        ls = {
            'listName': l[0],
            'contents': l[1],
            'isPersistent': False
        }
        lists.append(ls)

    blockComments = {}

    for key, c in target['comments'].items():
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
            blockComments[c['blockId']] = len(comments)

        comments.append(comment)
    
    blocks = target['blocks'] 
    blockID = 0

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
                setCommentBlockId(key)
                blockID += 1
                scripts.append(script)
                scriptCount += 1

        elif b['topLevel']:

            setCommentBlockId(key)
            block = b

            x = round(block['x'] / 1.5, 6)
            if x % 1 == 0:
                x = int(x)
            y = round(block['y'] / 1.8, 6)
            if y % 1 == 0:
                y = int(y)
            script = [x, y, []]

            end = False
            while not end:
                script[2].append(convert(block, blocks))
                if block['next'] == None:
                    end = True
                else:
                    setCommentBlockId(block['next'])
                    block = blocks[block['next']]
            
            scripts.append(script)
            scriptCount += 1
    
    sprite['scripts'] = scripts
    sprite['variables'] = variables
    sprite['lists'] = lists
    sprite['sounds'] = sounds
    sprite['costumes'] = costumes
    sprite['scriptComments'] = comments

    if isStage:

        sprite['currentCostumeIndex'] = target['currentCostume']
        sprite['tempoBPM'] = target['tempo']
        sprite['videoAlpha'] = (100 - target['videoTransparency']) / 100

        output = sprite
        output['objName'] = 'Stage'
        output['info'] = {
            'userAgent': data['meta']['agent'],
            'videoOn': target['videoState'] == 'on'
        }

    else:

        sprite['currentCostumeIndex'] = target['currentCostume']
        sprite['scratchX'] = target['x']
        sprite['scratchY'] = target['y']
        sprite['scale'] = target['size'] / 100
        sprite['direction'] = target['direction']
        sprite['rotationStyle'] = rotationStyles[target['rotationStyle']]
        sprite['isDraggable'] = target['draggable']
        sprite['indexInLibrary'] = targetsDone
        sprite['visible'] = target['visible']
        sprite['spriteInfo'] = {}

        sprites.append(sprite)

    targetsDone += 1
    print("Finished converting '{}' ({}/{})".format(sprite['objName'], targetsDone, totalTargets))

output['info']['scriptCount'] = scriptCount
output['info']['spriteCount'] = totalTargets - 1

monitors = []

lists = {}

for m in data['monitors']:
    if m['opcode'] == 'data_variable':
        
        sMin = m['min'] if 'min' in m else m['sliderMin']
        sMax = m['max'] if 'max' in m else m['sliderMax']
        monitor = {
            'target': 'Stage' if m['spriteName'] == None else m['spriteName'],
            'cmd': 'getVar:',
            'param': m['params']['VARIABLE'],
            'color': 15629590,
            'label': ("" if m['spriteName'] == None else (m['spriteName'] + ": ")) + m['params']['VARIABLE'],
            'mode': varModes[m['mode']],
            'sliderMin': sMin,
            'sliderMax': sMax,
            'isDiscrete': sMin % 1 == 0 and sMax % 1 == 0 and not('.' in str(sMin)) and not('.' in str(sMax)),
            'x': m['x'],
            'y': m['y'],
            'visible': m['visible']
        }
        monitors.append(monitor)

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

        monitors.append(monitor)

        spriteName = 'Stage' if m['spriteName'] == None else m['spriteName']
        if not spriteName in lists:
            lists[spriteName] = {}

        lists[spriteName][monitor['listName']] = {
            'x': m['x'],
            'y': m['y'],
            'width': m['width'],
            'height': m['height'],
            'visible': m['visible']
        }

    else:
        printWarn("Stage monitor '{}' will not be converted".format(m['opcode']))

for l in output['lists']:

    if l['listName'] in lists['Stage']:
        ls = lists['Stage'][l['listName']]

        l['x'] = ls['x']
        l['y'] = ls['y']
        l['width'] = ls['width']
        l['height'] = ls['height']
        l['visible'] = ls['visible']

for s in sprites:
    spriteName = s['objName']

    if spriteName in lists:
        for l in s['lists']:

            if l['listName'] in lists[spriteName]:
                ls = lists[spriteName][l['listName']]

                l['x'] = ls['x']
                l['y'] = ls['y']
                l['width'] = ls['width']
                l['height'] = ls['height']
                l['visible'] = ls['visible']

sprites.extend(monitors)

output['children'] = sprites

if 'wedo2' in data['extensions']:
    output['info']['savedExtensions'] = [{'extensionName': 'LEGO WeDo 2.0'}]

output = json.dumps(output)

zfsb2.writestr('project.json', output)

if warnings == 0:
    print('Completed with no warnings')
elif warnings == 1:
    print('Completed with {} warning'.format(warnings))
else:
    print('Completed with {} warnings'.format(warnings))