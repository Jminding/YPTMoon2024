from vidstab import VidStab
import matplotlib.pyplot as plt

# Using defaults
stabilizer = VidStab(kp_method='GFTT')
stabilizer.stabilize(input_path='/Users/jminding/Library/CloudStorage/GoogleDrive-jaymin_ding@ryecountryday.org/Shared drives/YPT/ Surface of the Moon/103_MoonPhases2021.mp4', output_path='/Users/jminding/Library/CloudStorage/GoogleDrive-jaymin_ding@ryecountryday.org/Shared drives/YPT/ Surface of the Moon/103_MoonPhases2021_stabilized.avi')

stabilizer.plot_trajectory()
plt.show()

stabilizer.plot_transforms()
plt.show()

# # Using a specific keypoint detector
# stabilizer = VidStab(kp_method='ORB')
# stabilizer.stabilize(input_path='input_video.mp4', output_path='stable_video.avi')

# # Using a specific keypoint detector and customizing keypoint parameters
# stabilizer = VidStab(kp_method='FAST', threshold=42, nonmaxSuppression=False)
# stabilizer.stabilize(input_path='input_video.mov', output_path='stable_video.avi')