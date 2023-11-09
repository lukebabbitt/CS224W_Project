import pandas as pd

def txt_to_csv(input_filename, output_filename, col_names, ints, floats, calmap=False):
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    # initialize empty lists for each column
    data = []
    for i in range(len(col_names)):
        data.append([])

    # split each line into columns
    line_num = 0
    while line_num < len(lines):
        parts = lines[line_num].strip().split()

        # add each space separated string as a seperate feature
        if len(parts) == len(col_names) or calmap:
            for i in range(len(parts)):
                if i in floats:
                    data[i].append(float(parts[i]))
                elif i in ints:
                    data[i].append(int(parts[i]))
                else:
                    data[i].append(parts[i])
        

        # for calmap, we want to add next row as the points if there are any
        if ((len(parts) + 1) == len(col_names)) and calmap:
            num_points = int(parts[-1])
            if num_points > 0:
                line_num += 1
                points = []
                next_line = lines[line_num]
                sep = next_line.find(' ')
                while sep != -1:
                    # get point id
                    point_id = int(next_line[0:sep])
                    next_line = next_line[sep + 1:]
                    end = next_line.find(' ')

                    #get point distance
                    point_dist = float(next_line[0:end])
                    next_line = next_line[end + 1:]

                    points.append([point_id, point_dist])

                    sep = next_line.find(' ')

                data[len(col_names) - 1].append(points)
            else:
                data[len(col_names) - 1].append([])
            
        
        line_num += 1



    # create a DataFrame
    data_frame = {}
    for i in range(len(col_names)):
        data_frame[col_names[i]] = data[i]

    df = pd.DataFrame(data_frame)

    # save the DataFrame as a CSV file
    df.to_csv(output_filename, index=False)



# transform 5 cal road data txt files to csv
txt_to_csv(input_filename='224w_data/calmap.txt', output_filename='224w_data/calmap.csv', col_names=['Start_Node_ID', 'End_Node_ID', 'Edge_Length', 'Num_Points_on_Edge', 'Points'], ints=[0, 1, 3], floats=[2], calmap=True)
txt_to_csv(input_filename='224w_data/CA.txt', output_filename='224w_data/CA.csv', col_names=['Category_Name', 'Longitude', 'Latitude'], ints=[], floats=[1, 2])
txt_to_csv(input_filename='224w_data/cal.cedge.txt', output_filename='224w_data/cal.cedge.csv', col_names=['Edge_ID', 'Start_Node_ID', 'End_Node_ID', 'L2_Distance'], ints=[0, 1, 2], floats=[3])
txt_to_csv(input_filename='224w_data/cal.cnode.txt', output_filename='224w_data/cal.cnode.csv', col_names=['Node_ID', 'Longitude', 'Latitude'], ints=[0], floats=[1, 2])
txt_to_csv(input_filename='224w_data/caldata.txt', output_filename='224w_data/caldata.csv', col_names=['Longitude', 'Latitude', 'Category_ID'], ints=[2], floats=[0, 1])