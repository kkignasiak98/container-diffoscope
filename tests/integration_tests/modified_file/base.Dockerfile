FROM alpine:3.21.3

RUN mkdir -p /temp_test_folder && \
    echo "original content" > /temp_test_folder/test_file.txt
