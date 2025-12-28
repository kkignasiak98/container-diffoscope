FROM base

RUN cd / && \
    mkdir -p temp_test_folder/temp_test_child_folder && \
    touch temp_test_folder/temp_test_child_folder/test_file.txt
