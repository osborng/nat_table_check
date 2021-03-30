FROM osborng/ubuntu_focal_python

# Set correct environment variables.
#ENV HOME /root
#ENV PYTHONUNBUFFERED=1

# Use baseimage-docker's init process.
ENTRYPOINT ["python"]
CMD ["/home/app/pyapp/nat_table_check_v2.py"]

# If you're using the 'customizable' variant, you need to explicitly opt-in
# for features.
#
RUN mkdir /home/app/pyapp
COPY --chown=app:app nat_table_check_v2.py /home/app/pyapp
RUN chmod +x /home/app/pyapp/*