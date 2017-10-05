#############################################################################
# Generated by PAGE version 4.9
# in conjunction with Tcl version 8.6
set vTcl(timestamp) ""


set vTcl(actual_gui_bg) #d9d9d9
set vTcl(actual_gui_fg) #000000
set vTcl(actual_gui_menu_bg) #d9d9d9
set vTcl(actual_gui_menu_fg) #000000
set vTcl(complement_color) #d9d9d9
set vTcl(analog_color_p) #d9d9d9
set vTcl(analog_color_m) #d9d9d9
set vTcl(active_fg) #000000
set vTcl(actual_gui_menu_active_bg)  #d8d8d8
set vTcl(active_menu_fg) #000000
#################################
#LIBRARY PROCEDURES
#


if {[info exists vTcl(sourcing)]} {

proc vTcl:project:info {} {
    set base .top37
    namespace eval ::widgets::$base {
        set dflt,origin 0
        set runvisible 1
    }
    set site_3_0 $base.fra37
    namespace eval ::widgets_bindings {
        set tagslist _TopLevel
    }
    namespace eval ::vTcl::modules::main {
        set procs {
        }
        set compounds {
        }
        set projectType single
    }
}
}

#################################
# USER DEFINED PROCEDURES
#

#################################
# GENERATED GUI PROCEDURES
#

proc vTclWindow.top37 {base} {
    if {$base == ""} {
        set base .top37
    }
    if {[winfo exists $base]} {
        wm deiconify $base; return
    }
    set top $base
    ###################
    # CREATING WIDGETS
    ###################
    vTcl::widgets::core::toplevel::createCmd $top -class Toplevel \
        -borderwidth 1 -background {#fcc63f} -highlightbackground {#d9d9d9} \
        -highlightcolor black 
    wm focusmodel $top passive
    wm geometry $top 1000x480+500+294
    update
    # set in toplevel.wgt.
    global vTcl
    set vTcl(save,dflt,origin) 0
    wm maxsize $top 1914 1045
    wm minsize $top 148 1
    wm overrideredirect $top 0
    wm resizable $top 0 0
    wm deiconify $top
    wm title $top "Nationale Spoorwegen Defect / Monteur Overzicht"
    vTcl:DefineAlias "$top" "Toplevel" vTcl:Toplevel:WidgetProc "" 1
    frame $top.fra37 \
        -borderwidth 2 -relief groove -background {#fcc63f} -height 495 \
        -highlightbackground {#d9d9d9} -highlightcolor black -width 1015 
    vTcl:DefineAlias "$top.fra37" "Frame1" vTcl:WidgetProc "Toplevel" 1
    set site_3_0 $top.fra37
    button $site_3_0.but43 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -pady 0 -text Button 
    vTcl:DefineAlias "$site_3_0.but43" "Button1" vTcl:WidgetProc "Toplevel" 1
    entry $site_3_0.ent44 \
        -background white -disabledforeground {#a3a3a3} -font TkFixedFont \
        -foreground {#000000} -insertbackground black 
    vTcl:DefineAlias "$site_3_0.ent44" "Entry1" vTcl:WidgetProc "Toplevel" 1
    button $site_3_0.but45 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -pady 0 -text Button 
    vTcl:DefineAlias "$site_3_0.but45" "Button2" vTcl:WidgetProc "Toplevel" 1
    place $site_3_0.but43 \
        -in $site_3_0 -x 0 -y 0 -width 126 -relwidth 0 -height 53 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.ent44 \
        -in $site_3_0 -x 230 -y 0 -width 254 -relwidth 0 -height 44 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.but45 \
        -in $site_3_0 -x 480 -y 0 -width 116 -relwidth 0 -height 43 \
        -relheight 0 -anchor nw -bordermode ignore 
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.fra37 \
        -in $top -x 0 -y 0 -width 1000 -relwidth 0 -height 480 -relheight 0 \
        -anchor nw -bordermode ignore 

    vTcl:FireEvent $base <<Ready>>
}

#############################################################################
## Binding tag:  _TopLevel

bind "_TopLevel" <<Create>> {
    if {![info exists _topcount]} {set _topcount 0}; incr _topcount
}
bind "_TopLevel" <<DeleteWindow>> {
    if {[set ::%W::_modal]} {
                vTcl:Toplevel:WidgetProc %W endmodal
            } else {
                destroy %W; if {$_topcount == 0} {exit}
            }
}
bind "_TopLevel" <Destroy> {
    if {[winfo toplevel %W] == "%W"} {incr _topcount -1}
}

Window show .
Window show .top37

