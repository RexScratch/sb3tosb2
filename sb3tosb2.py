import sys, json, zipfile, os

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
        output.append(hexToDec(inputVal('COLOR', block, blocks)))
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
        output.append(hexToDec(inputVal('COLOR', block, blocks)))
        return output

    @staticmethod
    def sensing_coloristouchingcolor(block, blocks):
        output = ['color:sees:']
        output.append(hexToDec(inputVal('COLOR', block, blocks)))
        output.append(hexToDec(inputVal('COLOR2', block, blocks)))
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
        block = blocks[block['inputs']['custom_block'][1]]
        procData = block['mutation']
        output = ['procDef']
        output.append(procData['proccode'])
        output.append(json.loads(procData['argumentnames']))
        output.append(json.loads(procData['argumentdefaults']))
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

Blocks.funcs = {
    "motion_movesteps": Blocks.motion_movesteps,
    "motion_turnright": Blocks.motion_turnright,
    "motion_turnleft": Blocks.motion_turnleft,
    "motion_pointindirection": Blocks.motion_pointindirection,
    "motion_pointtowards": Blocks.motion_pointtowards,
    "motion_gotoxy": Blocks.motion_gotoxy,
    "motion_goto": Blocks.motion_goto,
    "motion_glidesecstoxy": Blocks.motion_glidesecstoxy,
    "motion_changexby": Blocks.motion_changexby,
    "motion_setx": Blocks.motion_setx,
    "motion_changeyby": Blocks.motion_changeyby,
    "motion_sety": Blocks.motion_sety,
    "motion_ifonedgebounce": Blocks.motion_ifonedgebounce,
    "motion_setrotationstyle": Blocks.motion_setrotationstyle,
    "motion_xposition": Blocks.motion_xposition,
    "motion_yposition": Blocks.motion_yposition,
    "motion_direction": Blocks.motion_direction,
    "motion_scroll_right": Blocks.motion_scroll_right,
    "motion_scroll_up": Blocks.motion_scroll_up,
    "motion_align_scene": Blocks.motion_align_scene,
    "motion_xscroll": Blocks.motion_xscroll,
    "motion_yscroll": Blocks.motion_yscroll,

    "looks_sayforsecs": Blocks.looks_sayforsecs,
    "looks_say": Blocks.looks_say,
    "looks_thinkforsecs": Blocks.looks_thinkforsecs,
    "looks_think": Blocks.looks_think,
    "looks_show": Blocks.looks_show,
    "looks_hide": Blocks.looks_hide,
    "looks_hideallsprites": Blocks.looks_hideallsprites,
    "looks_switchcostumeto": Blocks.looks_switchcostumeto,
    "looks_nextcostume": Blocks.looks_nextcostume,
    "looks_switchbackdropto": Blocks.looks_switchbackdropto,
    "looks_changeeffectby": Blocks.looks_changeeffectby,
    "looks_seteffectto": Blocks.looks_seteffectto,
    "looks_cleargraphiceffects": Blocks.looks_cleargraphiceffects,
    "looks_changesizeby": Blocks.looks_changesizeby,
    "looks_setsizeto": Blocks.looks_setsizeto,
    "looks_changestretchby": Blocks.looks_changestretchby,
    "looks_setstretchto": Blocks.looks_setstretchto,
    "looks_gotofrontback": Blocks.looks_gotofrontback,
    "looks_goforwardbackwardlayers": Blocks.looks_goforwardbackwardlayers,
    "looks_costumenumbername": Blocks.looks_costumenumbername,
    "looks_backdropnumbername": Blocks.looks_backdropnumbername,
    "looks_size": Blocks.looks_size,
    "looks_switchbackdroptoandwait": Blocks.looks_switchbackdroptoandwait,
    "looks_nextbackdrop": Blocks.looks_nextbackdrop,

    "sound_play": Blocks.sound_play,
    "sound_playuntildone": Blocks.sound_playuntildone,
    "sound_stopallsounds": Blocks.sound_stopallsounds,
    "sound_changevolumeby": Blocks.sound_changevolumeby,
    "sound_setvolumeto": Blocks.sound_setvolumeto,
    "sound_volume": Blocks.sound_volume,

    "music_playDrumForBeats": Blocks.music_playDrumForBeats,
    "music_midiPlayDrumForBeats": Blocks.music_midiPlayDrumForBeats,
    "music_restForBeats": Blocks.music_restForBeats,
    "music_playNoteForBeats": Blocks.music_playNoteForBeats,
    "music_setInstrument": Blocks.music_setInstrument,
    "music_midiSetInstrument": Blocks.music_midiSetInstrument,
    "music_changeTempo": Blocks.music_changeTempo,
    "music_setTempo": Blocks.music_setTempo,
    "music_getTempo": Blocks.music_getTempo,

    "pen_clear": Blocks.pen_clear,
    "pen_stamp": Blocks.pen_stamp,
    "pen_penDown": Blocks.pen_penDown,
    "pen_penUp": Blocks.pen_penUp,
    "pen_setPenColorToColor": Blocks.pen_setPenColorToColor,
    "pen_changePenHueBy": Blocks.pen_changePenHueBy,
    "pen_setPenHueToNumber": Blocks.pen_setPenHueToNumber,
    "pen_changePenShadeBy": Blocks.pen_changePenShadeBy,
    "pen_setPenShadeToNumber": Blocks.pen_setPenShadeToNumber,
    "pen_changePenSizeBy": Blocks.pen_changePenSizeBy,
    "pen_setPenSizeTo": Blocks.pen_setPenSizeTo,
    "pen_setPenColorParamTo": Blocks.pen_setPenColorParamTo,
    "pen_changePenColorParamBy": Blocks.pen_changePenColorParamBy,

    "event_whenflagclicked": Blocks.event_whenflagclicked,
    "event_whenkeypressed": Blocks.event_whenkeypressed,
    "event_whenthisspriteclicked": Blocks.event_whenthisspriteclicked,
    "event_whenbackdropswitchesto": Blocks.event_whenbackdropswitchesto,
    "event_whengreaterthan": Blocks.event_whengreaterthan,
    "event_whenbroadcastreceived": Blocks.event_whenbroadcastreceived,
    "event_broadcast": Blocks.event_broadcast,
    "event_broadcastandwait": Blocks.event_broadcastandwait,

    "control_wait": Blocks.control_wait,
    "control_repeat": Blocks.control_repeat,
    "control_forever": Blocks.control_forever,
    "control_if": Blocks.control_if,
    "control_if_else": Blocks.control_if_else,
    "control_wait_until": Blocks.control_wait_until,
    "control_repeat_until": Blocks.control_repeat_until,
    "control_while": Blocks.control_while,
    "control_for_each": Blocks.control_for_each,
    "control_stop": Blocks.control_stop,
    "control_start_as_clone": Blocks.control_start_as_clone,
    "control_create_clone_of": Blocks.control_create_clone_of,
    "control_delete_this_clone": Blocks.control_delete_this_clone,
    "control_get_counter": Blocks.control_get_counter,
    "control_incr_counter": Blocks.control_incr_counter,
    "control_clear_counter": Blocks.control_clear_counter,
    "control_all_at_once": Blocks.control_all_at_once,

    "videoSensing_videoOn": Blocks.videoSensing_videoOn,
    "videoSensing_whenMotionGreaterThan": Blocks.videoSensing_whenMotionGreaterThan,
    "videoSensing_videoToggle": Blocks.videoSensing_videoToggle,
    "videoSensing_setVideoTransparency": Blocks.videoSensing_setVideoTransparency,

    "sensing_touchingobject": Blocks.sensing_touchingobject,
    "sensing_touchingcolor": Blocks.sensing_touchingcolor,
    "sensing_coloristouchingcolor": Blocks.sensing_coloristouchingcolor,
    "sensing_distanceto": Blocks.sensing_distanceto,
    "sensing_askandwait": Blocks.sensing_askandwait,
    "sensing_answer": Blocks.sensing_answer,
    "sensing_keypressed": Blocks.sensing_keypressed,
    "sensing_mousedown": Blocks.sensing_mousedown,
    "sensing_mousex": Blocks.sensing_mousex,
    "sensing_mousey": Blocks.sensing_mousey,
    "sensing_loudness": Blocks.sensing_loudness,
    "sensing_loud": Blocks.sensing_loud,
    "sensing_timer": Blocks.sensing_timer,
    "sensing_resettimer": Blocks.sensing_resettimer,
    "sensing_of": Blocks.sensing_of,
    "sensing_current": Blocks.sensing_current,
    "sensing_dayssince2000": Blocks.sensing_dayssince2000,
    "sensing_username": Blocks.sensing_username,
    "sensing_userid": Blocks.sensing_userid,

    "operator_add": Blocks.operator_add,
    "operator_subtract": Blocks.operator_subtract,
    "operator_multiply": Blocks.operator_multiply,
    "operator_divide": Blocks.operator_divide,
    "operator_random": Blocks.operator_random,
    "operator_gt": Blocks.operator_gt,
    "operator_lt": Blocks.operator_lt,
    "operator_equals": Blocks.operator_equals,
    "operator_and": Blocks.operator_and,
    "operator_or": Blocks.operator_or,
    "operator_not": Blocks.operator_not,
    "operator_join": Blocks.operator_join,
    "operator_letter_of": Blocks.operator_letter_of,
    "operator_length": Blocks.operator_length,
    "operator_mod": Blocks.operator_mod,
    "operator_round": Blocks.operator_round,
    "operator_mathop": Blocks.operator_mathop,

    "data_variable": Blocks.data_variable,
    "data_setvariableto": Blocks.data_setvariableto,
    "data_changevariableby": Blocks.data_changevariableby,
    "data_showvariable": Blocks.data_showvariable,
    "data_hidevariable": Blocks.data_hidevariable,
    "data_listconents": Blocks.data_listcontents,
    "data_addtolist": Blocks.data_addtolist,
    "data_deleteoflist": Blocks.data_deleteoflist,
    "data_deletealloflist": Blocks.data_deletealloflist,
    "data_insertatlist": Blocks.data_insertatlist,
    "data_replaceitemoflist": Blocks.data_replaceitemoflist,
    "data_itemoflist": Blocks.data_itemoflist,
    "data_lengthoflist": Blocks.data_lengthoflist,
    "data_listcontainsitem": Blocks.data_listcontainsitem,   
    "data_showlist": Blocks.data_showlist,
    "data_hidelist": Blocks.data_hidelist,

    "procedures_definition": Blocks.procedures_definition,
    "procedures_call": Blocks.procedures_call,
    "argument_reporter_string_number": Blocks.argument_reporter_string_number,
    "argument_reporter_boolean": Blocks.argument_reporter_boolean,
}

warnings = 0
blockID = 0
blockIDDelta = 0

def printWarn(message):
    global warnings
    print("WARNING: " + message)
    warnings += 1

def setCommentBlockId(id):
    global blockID, comments, blockComments
    if id in blockComments:
        comments[blockComments[id]][5] = blockID

def hexToDec(dec):
    try:
        return int(dec[1:], 16)
    except:
        return dec

def convert(block, blocks):
    global blockIDDelta
    opcode = block['opcode']
    if opcode in Blocks.funcs:
        blockIDDelta += 1
        return Blocks.funcs[opcode](block, blocks)
    elif len(block['inputs']) == 0 and len(block['fields']) == 1 and opcode != 'sensing_setdragmode': # Menu opcodes
        return fieldVal(list(block['fields'].items())[0][0], block)
    else:
        blockIDDelta += 1
        printWarn("Incompatible opcode '{}'".format(opcode))
        
        output = [opcode]
        for i in block['inputs']:
            output.append(inputVal(i, block, blocks))
        for f in block['fields']:
            output.append(fieldVal(f, block))
        return output

def topConvert(block, blocks):
    global blockID, blockIDDelta
    blockIDDelta = 0
    result = convert(block, blocks)
    blockID += blockIDDelta
    return result

def inputVal(value, block, blocks):

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
                return ['readVariable', out[1]]
            elif out[0] == 13:
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

    if output == '-Infinity':
        output = float('-inf')
    if output == 'Infinity':
        output = float('inf')

    return output

def fieldVal(value, block):

    if not value in block['fields']:
        return None

    return block['fields'][value][0]

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
        script.append(topConvert(block, blocks))
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

sb2path = sb2path[0:-4] + '(temp).zip'
try:
    os.remove(sb2path)
except:
    pass
zfsb2 = zipfile.ZipFile(sb2path, 'x')

sb3path = sys.argv[1]
sb3path = sb3path[0:-3] + 'zip'
try:
    os.rename(sys.argv[1], sb3path)
except:
    sys.argv[1] = sb3path[0:-3] + 'sb3'

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

for i in range(len(data['targets'])):

    blockID = 0

    target = data['targets'][i]
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
                img = img.replace("\\'", "'")
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
        comment.append(c['x'])
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

    for key, b in blocks.items():

        if type(b) == list:

            setCommentBlockId(key)

            y = round(b[4] / 1.8, 6)
            if y % 1 == 0:
                y = int(y)
            script = [b[3], y]

            if b[0] == 12:
                script.append([['readVariable', b[1]]])
            elif b[0] == 13:
                script.append([['contentsOfList:', b[1]]])
            else:
                script = None

            if script != None:
                blockID += 1
                scripts.append(script)
                scriptCount += 1

        elif b['topLevel']:

            setCommentBlockId(key)
            block = b

            y = round(block['y'] / 1.8, 6)
            if y % 1 == 0:
                y = int(y)
            script = [block['x'], y, []]

            end = False
            while not end:
                script[2].append(topConvert(block, blocks))
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
        sprite['indexInLibrary'] = i
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

output = json.dumps(output)

zfsb2.writestr('project.json', output)

zfsb3.close()
os.rename(sb3path, sys.argv[1])

zfsb2.close()
os.rename(sb2path, sys.argv[2])

if warnings == 0:
    print('Completed with no warnings')
elif warnings == 1:
    print('Completed with {} warning'.format(warnings))
else:
    print('Completed with {} warnings'.format(warnings))