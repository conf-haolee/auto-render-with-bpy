# import halconpy as ha
import halcon as ha
import pandas as pd
class RealRingDetector:
    def __init__(self, real_ring_image_path = ""):
        # self.model = load_model(model_path)
        self._real_ring_image_path = real_ring_image_path

    @property
    def real_ring_image_path(self):
        return self._real_ring_image_path
    @real_ring_image_path.setter
    def real_ring_image_path(self, real_ring_image_path):
        self._real_ring_image_path = real_ring_image_path

    def detect(self):
        # Initialize an empty DataFrame
        df = pd.DataFrame(columns=['Max Radius', 'Min Radius'])

        # Image Acquisition: Load image files
        image_files = ha.list_files(self._real_ring_image_path, ['files', 'follow_links'])
        image_files = [f for f in image_files if f.lower().endswith(('tif', 'tiff', 'gif', 'bmp', 'jpg', 'jpeg', 'jp2', 'png', 'pcx', 'pgm', 'ppm', 'pbm', 'xwd', 'ima', 'hobj'))]

        # Loop through all image files
        for image_file in image_files:
            # Read the image
            image = ha.read_image(image_file)
            
            # Convert to grayscale
            gray_image = ha.rgb1_to_gray(image)
            
            # Threshold to segment the image
            region = ha.threshold(gray_image, 0, 120)
            
            # Connect regions
            connected_regions = ha.connection(region)
            
            # Select regions based on shape features (roundness, circularity, ratio, area of holes)
            selected_regions = ha.select_shape(connected_regions, ['roundness', 'circularity', 'ratio', 'area_holes'], 
                                            'and', [0.7, 0.65, 0.8, 1500], [1, 1, 1.2, 4000])
            
            # Count the number of selected objects
            number_of_objects = ha.count_obj(selected_regions)
            
            # Loop through each selected object and calculate radii
            for i in range(1, number_of_objects + 1):
                object_selected = ha.select_obj(selected_regions, i)
                
                # Find smallest enclosing circle for the selected object (Max Radius)
                row1, column1, radius1 = ha.smallest_circle(object_selected)

                radius1 = radius1[0]  # Extract the scalar value from the tuple
                # Calculate the radius of holes inside the ring (Min Radius)
                region_fill_up = ha.fill_up(object_selected)
                region_difference = ha.difference(region_fill_up, object_selected)
                row, column, radius = ha.smallest_circle(region_difference)
                radius = radius[0]  # Extract the scalar value from the tuple

                # Create a temporary DataFrame with the new row
                temp_df = pd.DataFrame({'Max Radius': [radius1], 'Min Radius': [radius]})
                
                # Concatenate the new row with the existing DataFrame
                df = pd.concat([df, temp_df], ignore_index=True)


        # Calculate and print the average radii
        outer_circle_radius = df['Max Radius'].mean()
        inner_circle_radius = df['Min Radius'].mean()
        # print("Average Max Radius:", outer_circle_radius)
        # print("Average Min Radius:", inner_circle_radius)
        return outer_circle_radius, inner_circle_radius
    
        # Optionally, save to a CSV file
        # df.to_csv(datetime.now().strftime("%Y%m%d %H%M") + 'output_radii.csv', index=False)

