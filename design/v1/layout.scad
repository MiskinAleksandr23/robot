// Provisional envelope model. NOT printable production parts.
// All coordinates in mm: X across, Y forward, Z up.
show_shells = true;
show_parts = true;
$fn = 32;
if (show_shells) color([0.75,0.75,0.75,0.12]) translate([0, 0, 94]) cube([84, 58, 60], center=true); // body_shell
if (show_shells) color([0.75,0.75,0.75,0.12]) translate([0, 0, 171]) cube([76, 38, 42], center=true); // head_shell
if (show_shells) color([0.75,0.75,0.75,0.12]) translate([-29, 0, 7]) cube([48, 68, 14], center=true); // sole_l
if (show_shells) color([0.75,0.75,0.75,0.12]) translate([29, 0, 7]) cube([48, 68, 14], center=true); // sole_r
if (show_parts) color([0.7411764705882353, 0.48627450980392156, 0.2823529411764706]) translate([-22, 0, 81]) cube([34, 15, 30], center=true); // hip_l
if (show_parts) color([0.7411764705882353, 0.48627450980392156, 0.2823529411764706]) translate([22, 0, 81]) cube([34, 15, 30], center=true); // hip_r
if (show_parts) color([0.5098039215686274, 0.6, 0.4470588235294118]) translate([0, 0, 107]) cube([50, 30, 18], center=true); // battery
if (show_parts) color([0.3843137254901961, 0.5490196078431373, 0.6274509803921569]) translate([0, -22, 105]) cube([65, 6, 30], center=true); // pi
if (show_parts) color([0.3843137254901961, 0.5490196078431373, 0.6274509803921569]) translate([0, 22, 108]) cube([52, 7, 28], center=true); // esp32
if (show_parts) color([0.7098039215686275, 0.6039215686274509, 0.34901960784313724]) translate([0, -18, 76]) cube([50, 17, 10], center=true); // servo_bec
if (show_parts) color([0.7098039215686275, 0.6039215686274509, 0.34901960784313724]) translate([0, 18, 75]) cube([43, 17, 7], center=true); // logic_bec
if (show_parts) color([0.3843137254901961, 0.5490196078431373, 0.6274509803921569]) translate([0, 0, 120]) cube([20, 16, 4], center=true); // imu
if (show_parts) color([0.6431372549019608, 0.5607843137254902, 0.6509803921568628]) translate([35, 0, 108]) cube([3, 18, 18], center=true); // amp
if (show_parts) color([0.6431372549019608, 0.5607843137254902, 0.6509803921568628]) translate([-35, 0, 108]) cube([3, 14, 18], center=true); // mic
if (show_parts) color([0.6431372549019608, 0.5607843137254902, 0.6509803921568628]) translate([0, 24, 86]) cube([28, 5, 12], center=true); // speaker
if (show_parts) color([0.7411764705882353, 0.48627450980392156, 0.2823529411764706]) translate([0, 0, 137]) cube([23, 12, 29], center=true); // head_yaw
if (show_parts) color([0.7411764705882353, 0.48627450980392156, 0.2823529411764706]) translate([23, 0, 171]) cube([12, 23, 29], center=true); // head_pitch
if (show_parts) color([0.3843137254901961, 0.5490196078431373, 0.6274509803921569]) translate([0, 12, 171]) cube([25, 9, 24], center=true); // camera
if (show_parts) color([0.7411764705882353, 0.48627450980392156, 0.2823529411764706]) translate([-29, 0, 25]) cube([34, 29, 15], center=true); // foot_l
if (show_parts) color([0.7411764705882353, 0.48627450980392156, 0.2823529411764706]) translate([29, 0, 25]) cube([34, 29, 15], center=true); // foot_r
